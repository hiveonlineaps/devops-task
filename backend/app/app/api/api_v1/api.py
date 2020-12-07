from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, commitmentcategory, commitment, transaction, reputation, transaction, membership, groupreputation

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(commitmentcategory.router, prefix="/commitment-category", tags=["commitment category"])
api_router.include_router(membership.router, prefix="/membership", tags=["membership"])
api_router.include_router(commitment.router, prefix="/commitment", tags=["commitment"])
api_router.include_router(transaction.router, prefix="/transaction", tags=["transaction"])
api_router.include_router(reputation.router, prefix="/reputation", tags=["member reputation"])
api_router.include_router(groupreputation.router, prefix="/group-reputation", tags=["group reputation"])



