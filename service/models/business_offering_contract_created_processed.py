from dataclasses import dataclass, field
from typing import Optional


@dataclass(repr=True, frozen=True)
class Installment:
    description: str
    netAmountInstallment: float


@dataclass(repr=True, frozen=True)
class FinancialQuotation:
    quotationBusinessKey: str
    technicalResourceId: str
    validFrom: int
    validTo: int
    paymentReference: str
    installment: list[Installment] | None = field(default_factory=list)


@dataclass(order=True, repr=True, frozen=True)
class BusinessOfferingContractCreatedProcessed:
    idTransaction: str
    idRegister: Optional[str] = field(default='')
    contactBusinessKey: Optional[str] = field(default='')
    contactBusinessPartner: Optional[str] = field(default='')
    contractAccount: Optional[str] = field(default='')
    message: Optional[str] = field(default='')
    statusCode: Optional[str] = field(default='')
    applicationBusinessKey: Optional[str] = field(default='')
    companyCode: Optional[str] = field(default='')
    businessPlace: Optional[str] = field(default='')
    division: Optional[str] = field(default='')
    system: Optional[str] = field(default='')
    financialQuotation: FinancialQuotation | dict = field(default_factory=dict)

    def offer_id(self):
        try:
            if len(self.idTransaction.split('_')) > 1:
                offer_id = self.idTransaction.split('_')[2]
            if len(self.idTransaction.split('-')) > 1:
                offer_id = self.idTransaction.split('-')[2]

            return offer_id
        except IndexError as e:
            print(
                f'IdTransaction with wrong format or null: {e}:{self.idTransaction=}'
            )
            return 0
