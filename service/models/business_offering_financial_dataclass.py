from dataclasses import dataclass, field


@dataclass(order=True, repr=True)
class ScholarshipApplied:
    code: str
    value: str


@dataclass(order=True, repr=True)
class Installments:
    installment: str
    netValue: str
    scholarshipType: str
    ponctualityDiscountValue: str
    ponctualityDiscountNetValue: str
    scholarshipApplied: list[ScholarshipApplied]


@dataclass(order=True, repr=True)
class Scholarships:
    code: str
    untilEndProgram: str
    installmentFrom: str
    InstallmentTo: str


@dataclass(order=True, repr=True)
class BusinessOfferingFinancialContract:
    idRegister: str
    idTransaction: str
    system: field(default='Backbone')
    statusCode: str
    message: str
    contactBusinessKey: str
    applicationBusinessKey: str
    contactBusinessPartner: str
    contractAccount: str
    quotationBusinessKey: str
    paymentReference: str
    validFrom: str
    validTo: str
    semesterValue: str
    baseValue: str
    scholarship: list[Scholarships]
    installments: list[Installments]
