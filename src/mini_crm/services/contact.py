import random
import bisect

from mini_crm.repos import ContactRepo, OperatorRepo, SourceRepo, LeadRepo
from mini_crm.schemas import ContactCreateData, ContactFromDB, LeadCreateData, AssignedOperatorData


class ContactService:
    def __init__(self, repo: ContactRepo, 
                 operator_repo: OperatorRepo, 
                 source_repo: SourceRepo, 
                 lead_repo: LeadRepo) -> None:
        self.repo = repo
        self.operator_repo = operator_repo
        self.source_repo = source_repo
        self.lead_repo = lead_repo

    def choose_the_operator(self, operators: list[AssignedOperatorData]) -> AssignedOperatorData:
        # weighted random choice with binary search
        lookup = []
        total = 0
        for op in operators:
            total += op.weight
            lookup.append(total)
        random_number = random.randint(1, total)
        idx = bisect.bisect_left(lookup, random_number)

        return operators[idx]

    async def create_new_contact(self, data: ContactCreateData) -> ContactFromDB:
        # check the source exists
        source = await self.source_repo.get_by_id(data.source_id)

        # find or create lead
        lead = await self.lead_repo.get_by_email(data.lead_email)
        if not lead:
            lead_data = LeadCreateData(email=data.lead_email,
                                   first_name=data.lead_first_name,
                                   last_name=data.lead_last_name,
                                   )
            lead = await self.lead_repo.create(lead_data)

        # get all active assigned operators with weights and current capacity
        assigned_operators = await self.source_repo.get_assigned_operators(source.id)

        # create a list of available operators with weights and current capacity
        available_operators = []
        for op in assigned_operators:
            if op.current_capacity < op.operator.max_capacity and op.weight > 0:    
                available_operators.append(op)
        
        if not available_operators:
            # create a new 'open' contact with no operator assigned 
            await self.repo.create(source_id=source.id, lead_id=lead.id)
            raise Exception('Available operator not found, but your contact was created')
        
        # choose the operator from the list of available operators
        chosen_operator = self.choose_the_operator(available_operators)

        
        # create and return a new contact with assigned operator
        return await self.repo.create(source_id=source.id, lead_id=lead.id, operator_id=chosen_operator.operator.id)


    async def get_all_contacts(self) -> list[ContactFromDB]:
        return await self.repo.list_all()

    
