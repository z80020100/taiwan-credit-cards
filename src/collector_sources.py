"""Collector data sources and URL configurations."""

from typing import Final


class BankingAuthority:
    """Taiwan Banking Bureau data sources."""

    BASE_URL: Final[str] = "https://www.banking.gov.tw"
    DOMESTIC_BANKS_URL: Final[str] = (
        f"{BASE_URL}/ch/home.jsp?id=604&parentpath=0,555&mcustomize=FscSearch_RelatedLink.jsp&type=1"
    )
    CREDIT_CARD_COMPANIES_URL: Final[str] = (
        f"{BASE_URL}/ch/home.jsp?id=604&parentpath=0,555&mcustomize=FscSearch_RelatedLink.jsp&type=C"
    )


class BankSources:
    """Bank-specific data sources for credit card information."""

    class EsunBank:
        """E.SUN Bank (玉山銀行) data source."""

        BASE_URL: Final[str] = "https://www.esunbank.com"
        CREDIT_CARDS_URL: Final[str] = f"{BASE_URL}/zh-tw/personal/credit-card/intro"
        BANK_NAME: Final[str] = "玉山銀行"


class CollectorConfig:
    """Common configuration settings for all collectors."""

    TIMEOUT: Final[int] = 30
    USER_AGENT: Final[str] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    DISABLE_SSL_VERIFICATION: Final[bool] = True


class DataPaths:
    """File paths for storing collected data."""

    DATA_DIR: Final[str] = "data"
    CREDIT_CARDS_CSV: Final[str] = f"{DATA_DIR}/taiwan-credit-cards.csv"
    CARD_ISSUERS_CSV: Final[str] = f"{DATA_DIR}/taiwan-card-issuers.csv"
