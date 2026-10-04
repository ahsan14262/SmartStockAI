import pytest
from app.services.approvals import create_proposal,approve

def test_approval_invalidated_by_changed_inputs():
    p=create_proposal('price',{'price':10},{'cost':7})
    with pytest.raises(ValueError): approve(p,'owner',{'cost':8})
