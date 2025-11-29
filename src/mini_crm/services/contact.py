import random

from mini_crm.repos import ContactRepo
from mini_crm.schemas import ContactCreateData, ContactFromDB, LeadCreateData

from mini_crm.services.operator import OperatorService
from mini_crm.services.source import SourceService
from mini_crm.services.lead import LeadService
# from mini_crm.services import OperatorService, SourceService, LeadService

class ContactService:
    def __init__(self, repo: ContactRepo, 
                 operator_service: OperatorService, 
                 source_service: SourceService, 
                 lead_service: LeadService) -> None:
        self.repo = repo
        self.operator_service = operator_service
        self.source_service = source_service
        self.lead_service = lead_service


    async def create_new_contact(self, data: ContactCreateData) -> ContactFromDB:
        # check the source exists
        source = await self.source_service.get_source_by_id(data.source_id)

        # find or create lead
        lead = await self.lead_service.get_lead_by_email(data.lead_email)
        if not lead:
            lead_data = LeadCreateData(email=data.lead_email,
                                   first_name=data.lead_first_name,
                                   last_name=data.lead_last_name,
                                   )
            lead = await self.lead_service.create_new_lead(lead_data)

        # get all active assigned operators with weights and current capacity
        assigned_operators = await self.source_service.get_assigned_operators_for_source(source.id)

        # create a list of available operators with weights and current capacity
        available_operators = []
        for op in assigned_operators:
            if op.current_capacity < op.operator.max_capacity and op.weight > 0:    
                available_operators.append(op)
        
        if not available_operators:
            # create a new 'open' contact with no operator assigned 
            await self.repo.create(source_id=source.id, lead_id=lead.id)
            raise Exception('Available operator not found, but your contact was created')
        
        # weighted random choice
        total_weights = sum(op.weight for op in available_operators)
        random_number = random.uniform(0, total_weights)
        upto = 0
        chosen_operator = None
        for op in available_operators:
            upto += op.weight
            if random_number <= upto:
                chosen_operator = op
                break
        
        # create and return a new contact with assigned operator
        return await self.repo.create(source_id=source.id, lead_id=lead.id, operator_id=chosen_operator.operator.id)


    async def get_all_contacts(self) -> list[ContactFromDB]:
        return await self.repo.list_all()

    
