from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
import enum

db = SQLAlchemy()

class VulnerabilityType(enum.Enum):
    SOFTWARE = "software"
    HARDWARE = "hardware"
    NETWORK = "network"

class ProductEnvironment(enum.Enum):
    WEB = "web"
    BINARY = "binary"
    MOBILE = "mobile"
    CLOUD = "cloud"

class Vulnerability(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    cve_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    cvss_vector: Mapped[str] = mapped_column(nullable=False)
    cvss_score: Mapped[float] = mapped_column(nullable=False)
    cvss_severity: Mapped[str] = mapped_column(nullable=False)
    vulnerability_name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[VulnerabilityType] = mapped_column(Enum(VulnerabilityType), nullable=False)
    product_env: Mapped[ProductEnvironment] = mapped_column(Enum(ProductEnvironment), nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    product_vendor: Mapped[str] = mapped_column(nullable=False)
    product_version: Mapped[str] = mapped_column(nullable=False)
    product_link: Mapped[str] = mapped_column(nullable=False)
    reporter: Mapped[str] = mapped_column(nullable=False)
    report_date: Mapped[date] = mapped_column(nullable=False)
    disclose_date: Mapped[date] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f'{self.cve_id}'