from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.web import template_context, templates


router = APIRouter()


@router.get("/")
def home(
    request: Request,
    q: str = "",
    category: str = "",
    db: Session = Depends(get_db),
):
    query = (
        select(Product)
        .options(joinedload(Product.category))
        .where(Product.is_active.is_(True))
        .order_by(Product.is_featured.desc(), Product.created_at.desc())
    )
    if q.strip():
        search_term = f"%{q.strip()}%"
        query = query.where(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
            )
        )
    if category:
        query = query.join(Product.category).where(Category.slug == category)

    products = db.scalars(query).unique().all()
    categories = db.scalars(
        select(Category).where(Category.is_active.is_(True)).order_by(Category.name)
    ).all()
    return templates.TemplateResponse(
        request=request,
        name="store/index.html",
        context=template_context(
            request,
            products=products,
            categories=categories,
            selected_category=category,
            search_query=q,
        ),
    )


@router.get("/products/{slug}")
def product_detail(request: Request, slug: str, db: Session = Depends(get_db)):
    product = db.scalar(
        select(Product)
        .options(joinedload(Product.category))
        .where(Product.slug == slug, Product.is_active.is_(True))
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return templates.TemplateResponse(
        request=request,
        name="store/product_detail.html",
        context=template_context(request, product=product),
    )
