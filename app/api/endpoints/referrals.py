from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..deps import get_current_affiliate, get_db
from ...models import Referral, Affiliate
from ...schemas import Referral as ReferralSchema

router = APIRouter()

@router.get("/", response_model=List[ReferralSchema])
def read_referrals(
    db: Session = Depends(get_db),
    current_affiliate: Affiliate = Depends(get_current_affiliate),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by status (pending, converted, rejected)"),
) -> Any:
    """
    Retrieve referrals for current affiliate.
    """
    query = db.query(Referral).filter(Referral.affiliate_id == current_affiliate.id)
    if status:
        query = query.filter(Referral.status == status)
    
    referrals = query.order_by(Referral.referred_at.desc()).offset(skip).limit(limit).all()
    return referrals

@router.get("/{id}", response_model=ReferralSchema)
def read_referral(
    id: str,
    db: Session = Depends(get_db),
    current_affiliate: Affiliate = Depends(get_current_affiliate),
) -> Any:
    """
    Get referral by ID.
    """
    referral = db.query(Referral).filter(
        Referral.id == id, Referral.affiliate_id == current_affiliate.id
    ).first()
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")
    return referral
