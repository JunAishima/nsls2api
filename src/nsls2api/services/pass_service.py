from pydantic import ValidationError
from nsls2api.infrastructure import config
from nsls2api.infrastructure.logging import logger
from nsls2api.services.helpers import _call_async_webservice
from nsls2api.models.pass_models import PassCycle, PassProposal, PassProposalType

settings = config.get_settings()

api_key = settings.pass_api_key
base_url = settings.pass_api_url


async def get_proposal(proposal_id: int) -> PassProposal:
    url = f"{base_url}/Proposal/GetProposal/{api_key}/NSLS-II/{proposal_id}"

    try:
        raw_proposal = await _call_async_webservice(url)
        proposal = PassProposal(**raw_proposal)
    except ValidationError as e:
        logger.error(f"Error validating data recevied from PASS for proposal: {e}")
        proposal = None
    except Exception as e:
        logger.error(f"Error retrieving proposal from PASS: {e}")
        proposal = None

    return proposal


async def get_proposal_types() -> PassProposalType:
    url = f"{base_url}/Proposal/GetProposalTypes/{api_key}/NSLS-II"

    try:
        raw_proposal_types = await _call_async_webservice(url)
        proposal_types = []
        if raw_proposal_types:
            for proposal_type in raw_proposal_types:
                proposal_types.append(PassProposalType(**proposal_type))
    except ValidationError as e:
        logger.error(
            f"Error validating data recevied from PASS for proposal types: {e}"
        )
        proposal_types = None
    except Exception as e:
        logger.error(f"Error retrieving proposal types from PASS: {e}")
        proposal_types = None

    return proposal_types


async def get_saf_from_proposal(proposal_id: int):
    url = f"{base_url}/SAF/GetSAFsByProposal/{api_key}/NSLS-II/{proposal_id}"

    saf = await _call_async_webservice(url)
    return saf


async def get_commissioning_proposals_by_year(year: int):
    # The PASS ID for commissioning proposals is 300005
    url = f"{base_url}Proposal/GetProposalsByType/{api_key}/NSLS-II/{year}/300005/NULL"
    proposals = await _call_async_webservice(url)
    return proposals


async def get_pass_resources():
    url = f"{base_url}/Resource/GetResources/{api_key}/NSLS-II"
    resources = await _call_async_webservice(url)
    return resources


async def get_cycles() -> PassCycle:
    url = f"{base_url}/Proposal/GetCycles/{api_key}/NSLS-II"
    print(url)
    cycles = await _call_async_webservice(url)
    return PassCycle(**cycles)


async def get_proposals_allocated():
    url = f"{base_url}/Proposal/GetProposalsAllocated/{api_key}/NSLS-II"
    allocated_proposals = await _call_async_webservice(url)
    return allocated_proposals


async def get_proposals_by_person(bnl_id: str):
    url = f"{base_url}/Proposal/GetProposalsByPerson/{api_key}/NSLS-II/null/null/{bnl_id}/null"
    print(url)
    proposals = await _call_async_webservice(url)
    return proposals
