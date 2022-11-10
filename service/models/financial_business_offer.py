from dataclasses import dataclass
from typing import Union


@dataclass(repr=True)
class ScholarshipsInstallment:
    code: str
    value: str


@dataclass(repr=True)
class Installments:
    installment: str
    netValue: str
    ponctualityDiscountValue: str
    ponctualityDiscountNetValue: str
    scholarships: Union[ScholarshipsInstallment, list[ScholarshipsInstallment]]


@dataclass(order=True, repr=True, frozen=True)
class Scholarships:
    code: str
    description: str
    bitType: str
    scholarshipType: str
    scholarshipTypeDescription: str
    calculationBasis: str
    calculationBasisDescription: str
    calculationType: str
    calculationTypeDescription: str
    calculationOrder: str
    offerValue: str
    untilEndProgram: str
    installmentFrom: str
    InstallmentTo: str
    priority: str


@dataclass(order=True, repr=True, frozen=True)
class FinancialBusinessOffer:
    offerSimulationId: str
    subscriptionValue: str
    enrollmentValue: str
    baseValue: str
    offerValue: str
    ponctualityPercentage: str
    minimumValue: str
    firstValue: str
    gracePeriod: str
    expirationPeriod: str
    scholarships: list[Scholarships]
    installments: list[Installments]
