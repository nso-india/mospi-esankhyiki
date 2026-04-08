"""
MoSPI API Client
Handles all HTTP calls to the MoSPI data portal.
"""

import math
import random
import os
import ssl
import yaml
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class _LegacySSLAdapter(HTTPAdapter):
    """HTTPAdapter that enables legacy SSL renegotiation.

    The MoSPI API server requires legacy SSL renegotiation which is
    disabled by default in newer OpenSSL versions. This adapter creates
    an SSL context with OP_LEGACY_SERVER_CONNECT enabled.
    """

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


class MoSPI:
    """Unified client for all MoSPI dataset APIs."""

    def __init__(self, base_url: str = "https://api.mospi.gov.in"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
        retry = Retry(
            total=3,
            connect=2,
            read=2,
            status=3,
            backoff_factor=0.6,
            status_forcelist=sorted(RETRYABLE_STATUS_CODES),
            allowed_methods=frozenset({"GET", "POST"}),
            respect_retry_after_header=True,
        )
        adapter = _LegacySSLAdapter(max_retries=retry)
        self.session.verify = False
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.api_endpoints = {
            "PLFS": "/api/plfs/getData",
            "CPI_Group": "/api/cpi/getCPIIndex",
            "CPI_Item": "/api/cpi/getItemIndex",
            "IIP_Annual": "/api/iip/getIIPAnnual",
            "IIP_Monthly": "/api/iip/getIIPMonthly",
            "ASI": "/api/asi/getASIData",
            "NAS": "/api/nas/getNASData",
            "WPI": "/api/wpi/getWpiRecords",
            "Energy": "/api/energy/getEnergyRecords",
            "AISHE": "/api/aishe/getAisheRecords",
            "ASUSE": "/api/asuse/getAsuseRecords",
            "GENDER": "/api/gender/getGenderRecords",
            "NFHS": "/api/nfhs/getNfhsRecords",
            "ENVSTATS": "/api/env/getEnvStatsRecords",
            "RBI": "/api/rbi/getRbiRecords",
            "NSS77": "/api/nss-77/getNss77Records",
            "NSS78": "/api/nss-78/getNss78Records",
            "CPIALRL": "/api/cpialrl/getCpialrlRecords",
            "HCES": "/api/hces/getHcesRecords",
            "TUS": "/api/tus/getTusRecords",
        }

    def get_data(self, dataset_name: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Fetch data from a MoSPI dataset endpoint."""
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        # CPI base_year 2024 uses unified endpoint
        if dataset_name in ["CPI_Group", "CPI_Item"] and params and params.get("base_year") == "2024":
            full_url = f"{self.base_url}/api/cpi/getCPIData"
        else:
            endpoint_path = self.api_endpoints.get(dataset_name)
            if not endpoint_path:
                return {"error": f"Dataset '{dataset_name}' not found."}
            full_url = f"{self.base_url}{endpoint_path}"

        try:
            response = self.session.get(full_url, params=params, timeout=30)
            response.raise_for_status()

            format_param = params.get("Format", "JSON") if params else "JSON"
            if format_param == "CSV":
                return {"data": response.text, "format": "CSV"}
            else:
                return response.json()
        except Exception as e:
            return {"error": f"An error occurred: {e}"}

    # =========================================================================
    # PLFS
    # =========================================================================

    def get_plfs_indicators(self) -> Dict[str, Any]:
        result = {}
        try:
            for fc, label in [(1, "Annual"), (2, "Quarterly"), (3, "Monthly")]:
                response = self.session.get(
                    f"{self.base_url}/api/plfs/getIndicatorListByFrequency",
                    params={"frequency_code": fc}, timeout=30,
                )
                response.raise_for_status()
                data = response.json()
                result[f"frequency_code_{fc}_{label}"] = data.get("data", [])
            return {"indicators_by_frequency": result, "statusCode": True}
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_plfs_filters(self, indicator_code: int, frequency_code: int = 1,
                         year: Optional[str] = None, month_code: Optional[str] = None) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code, "frequency_code": frequency_code}
        if year:
            params["year"] = year
        if month_code:
            params["month_code"] = month_code
        try:
            response = self.session.get(
                f"{self.base_url}/api/plfs/getFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # CPI
    # =========================================================================

    def get_cpi_base_years(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/cpi/getCpiBaseYear", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_cpi_filters(self, base_year: str = "2024", level: str = "Group",
                        series_code: str = "Current") -> Dict[str, Any]:
        params = {"base_year": base_year, "level": level if level else "null", "series_code": series_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/cpi/getCpiFilterByLevelAndBaseYear", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # IIP
    # =========================================================================

    def get_iip_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/iip/getIipBaseYear", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_iip_filters(self, base_year: str = "2011-12", frequency: str = "Annually") -> Dict[str, Any]:
        params = {"base_year": base_year, "frequency": frequency}
        try:
            response = self.session.get(
                f"{self.base_url}/api/iip/getIipFilter", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # ASI
    # =========================================================================

    def get_asi_classification_years(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/asi/getNicClassificationYear", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_asi_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.base_url}/api/asi/getAsiFilter",
                params={"classification_year": "2008"}, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_asi_filters(self, classification_year: str = "2008") -> Dict[str, Any]:
        params = {"classification_year": classification_year}
        try:
            response = self.session.get(
                f"{self.base_url}/api/asi/getAsiFilter", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # NAS
    # =========================================================================

    def get_nas_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/nas/getNasIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nas_filters(self, series: str = "Current", frequency_code: int = 1,
                        indicator_code: int = 1, base_year: str = "2022-23") -> Dict[str, Any]:
        params = {
            "base_year": base_year, "series": series,
            "frequency_code": frequency_code, "indicator_code": indicator_code,
        }
        try:
            response = self.session.get(
                f"{self.base_url}/api/nas/getNasFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # WPI
    # =========================================================================

    def get_wpi_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/wpi/getWpiBaseYear", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_wpi_filters(self, base_year: str = "2011-12") -> Dict[str, Any]:
        params = {"base_year": base_year}
        try:
            response = self.session.get(
                f"{self.base_url}/api/wpi/getWpiData",
                params=params,
                timeout=60,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # Energy
    # =========================================================================

    def get_energy_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/energy/getEnergyIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_energy_filters(self, indicator_code: int = 1, use_of_energy_balance_code: int = 1) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code, "use_of_energy_balance_code": use_of_energy_balance_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/energy/getEnergyFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # AISHE
    # =========================================================================

    def get_aishe_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/aishe/getAisheIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_aishe_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/aishe/getAisheFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # ASUSE
    # =========================================================================

    def get_asuse_indicators(self, frequency_code: int = 1) -> Dict[str, Any]:
        url = f"{self.base_url}/api/asuse/getAsuseIndicatorListByFrequency"
        result = {}
        try:
            for fc, label in [(1, "Annual"), (2, "Quarterly")]:
                response = self.session.get(url, params={"frequency_code": fc}, timeout=30)
                response.raise_for_status()
                data = response.json()
                result[f"frequency_code_{fc}_{label}"] = data.get("data", [])
            return {
                "indicators_by_frequency": result,
                "_note": (
                    "frequency_code=1 (Annual) has 35 indicators. "
                    "frequency_code=2 (Quarterly) has 15 indicators. "
                    "Pass the correct frequency_code in get_metadata() and get_data()."
                ),
                "statusCode": True,
            }
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_asuse_filters(self, indicator_code: int, frequency_code: int = 1) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code, "frequency_code": frequency_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/asuse/getAsuseFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # GENDER
    # =========================================================================

    def get_gender_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/gender/getGenderIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_gender_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/gender/getGenderFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # NFHS
    # =========================================================================

    def get_nfhs_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/nfhs/getNfhsIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nfhs_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/nfhs/getNfhsFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # ENVSTATS
    # =========================================================================

    def get_envstats_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/env/getEnvStatsIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_envstats_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/env/getEnvStatsFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # RBI
    # =========================================================================

    def get_rbi_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/rbi/getRbiIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_rbi_filters(self, sub_indicator_code: int) -> Dict[str, Any]:
        params = {"sub_indicator_code": sub_indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/rbi/getRbiMetaData", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # NSS77
    # =========================================================================

    def get_nss77_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/nss-77/getIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nss77_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/nss-77/getFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # NSS78
    # =========================================================================

    def get_nss78_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/nss-78/getIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nss78_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/nss-78/getFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # CPIALRL
    # =========================================================================

    def get_cpialrl_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/cpialrl/getCpialrlIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_cpialrl_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/cpialrl/getCpialrlFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # HCES
    # =========================================================================

    def get_hces_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/hces/getHcesIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_hces_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/hces/getHcesFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # TUS
    # =========================================================================

    def get_tus_indicators(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.base_url}/api/tus/getTusIndicatorList", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_tus_filters(self, indicator_code: int) -> Dict[str, Any]:
        params = {"indicator_code": indicator_code}
        try:
            response = self.session.get(
                f"{self.base_url}/api/tus/getTusFilterByIndicatorId", params=params, timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # EC (Economic Census) - POST to esankhyiki.mospi.gov.in
    # =========================================================================

    _EC_URLS = {
        1: "https://esankhyiki.mospi.gov.in/EC/filterDistrict6",
        2: "https://esankhyiki.mospi.gov.in/EC/filterDistrict5",
        3: "https://esankhyiki.mospi.gov.in/EC/filterDistrict4",
    }
    _EC_SUBMIT_URLS = {
        1: "https://esankhyiki.mospi.gov.in/dashboard/EC/submitForm6",
        2: "https://esankhyiki.mospi.gov.in/dashboard/EC/submitForm5",
        3: "https://esankhyiki.mospi.gov.in/dashboard/EC/submitForm4",
    }
    _EC_VERSION_MAP = {1: "6", 2: "5", 3: "4"}
    _EC_SWAGGER_PATHS = {
        1: "/EC/filterDistrict6",
        2: "/EC/filterDistrict5",
        3: "/EC/filterDistrict4",
    }
    _EC_SUBMIT_SWAGGER_PATHS = {
        1: "/EC/submitForm6",
        2: "/EC/submitForm5",
        3: "/EC/submitForm4",
    }

    def get_ec_indicators(self) -> Dict[str, Any]:
        return {
            "data": [
                {"indicator_code": 1, "indicator_name": "Sixth Economic Census (EC6) - 2013-14",
                 "description": "District-wise establishment and worker counts. 36 States/UTs, 24 activity sectors."},
                {"indicator_code": 2, "indicator_name": "Fifth Economic Census (EC5) - 2005",
                 "description": "District-wise establishment and worker counts. 35 States/UTs, 313 NIC-based activity codes."},
                {"indicator_code": 3, "indicator_name": "Fourth Economic Census (EC4) - 1998",
                 "description": "District-wise establishment and worker counts. 35 States/UTs, 18 activity sectors."},
            ],
            "statusCode": True,
        }

    def get_ec_filters(self, indicator_code: int) -> Dict[str, Any]:
        swagger_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "swagger", "swagger_user_ec.yaml",
        )
        ranking_path = self._EC_SWAGGER_PATHS.get(indicator_code)
        detail_path = self._EC_SUBMIT_SWAGGER_PATHS.get(indicator_code)
        if not ranking_path:
            return {"error": f"Invalid indicator_code {indicator_code}. Use 1 (EC6), 2 (EC5), or 3 (EC4).", "statusCode": False}

        try:
            with open(swagger_path, "r") as f:
                spec = yaml.safe_load(f)

            ranking_params = spec["paths"][ranking_path]["get"]["parameters"]
            data = {}
            for p in ranking_params:
                name = p["name"]
                enum_names = p.get("x-enum-names", {})
                if enum_names:
                    data[name] = [{"id": code, "name": desc} for code, desc in sorted(enum_names.items())]

            detail_params = spec["paths"][detail_path]["get"]["parameters"]
            detail_param_names = [p["name"] for p in detail_params]

            return {
                "data": data,
                "ranking_mode_params": [p["name"] for p in ranking_params],
                "detail_mode_params": detail_param_names,
                "statusCode": True,
                "_note": (
                    "state is required. All other filters are optional. "
                    "Pass mode='ranking' for top/bottom N districts (uses top5opt). "
                    "Pass mode='detail' for row-level data (uses pageNum, 20 rows/page)."
                ),
            }
        except Exception as e:
            return {"error": str(e), "statusCode": False}

    def get_ec_data(self, indicator_code: int, filters: Dict[str, str]) -> Dict[str, Any]:
        if filters.get("mode") == "detail":
            return self._get_ec_detail_data(indicator_code=indicator_code, filters=filters)

        url = self._EC_URLS.get(indicator_code)
        ec_num = self._EC_VERSION_MAP.get(indicator_code)
        if not url:
            return {"error": f"Invalid indicator_code {indicator_code}. Use 1 (EC6), 2 (EC5), or 3 (EC4).", "statusCode": False}

        state = filters.get("state", "")
        if not state:
            return {"error": "state is required for EC queries.", "statusCode": False}

        form_data = {
            "ec": ec_num, "state": state, "param1": "val1",
            "top5opt": filters.get("top5opt", "2"),
            "nop": filters.get("nop", ""), "sof": filters.get("sof", ""),
            "activity": filters.get("activity", ""), "ownership": filters.get("ownership", ""),
            "sector": filters.get("sector", ""),
        }

        try:
            response = self.session.post(
                url, data=form_data,
                headers={"Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest"},
                timeout=30,
            )
            response.raise_for_status()
            raw = response.json()

            districts = []
            html = raw.get("code", "")
            if html:
                soup = BeautifulSoup(f"<table>{html}</table>", "html.parser")
                for row in soup.find_all("tr"):
                    cols = row.find_all("td")
                    if len(cols) == 3:
                        districts.append({
                            "rank": cols[0].get_text(strip=True),
                            "district": cols[1].get_text(strip=True),
                            "establishments": cols[2].get_text(strip=True),
                        })

            return {
                "data": districts,
                "summary": {
                    "total_establishments": raw.get("counter"),
                    "total_workers": raw.get("wcounter"),
                    "max_establishments": raw.get("max_ent"),
                    "min_establishments": raw.get("min_ent"),
                    "max_workers": raw.get("max_workers"),
                    "min_workers": raw.get("min_workers"),
                },
                "description": raw.get("msgText", ""),
                "statusCode": True,
            }
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def _get_ec_detail_data(self, indicator_code: int, filters: Dict[str, str]) -> Dict[str, Any]:
        url = self._EC_SUBMIT_URLS.get(indicator_code)
        ec_num = self._EC_VERSION_MAP.get(indicator_code)
        if not url:
            return {"error": f"Invalid indicator_code {indicator_code}.", "statusCode": False}

        page_num = filters.get("pageNum", "1")
        form_data = {
            "ec": ec_num, "state": filters.get("state", ""),
            "nop": filters.get("nop", ""), "sof": filters.get("sof", ""),
            "activity": filters.get("activity", ""), "randomnum": str(random.random()),
            "pageNum": str(page_num), "ownership": filters.get("ownership", ""),
            "sector": filters.get("sector", ""),
        }

        try:
            response = self.session.post(
                url, data=form_data,
                headers={"Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest"},
                timeout=30,
            )
            response.raise_for_status()
            raw = response.json()

            col_maps = {
                1: {
                    "sl_no": 0, "state": 1, "sector": 2, "district": 3,
                    "household_type": 4, "activity": 5, "nature_of_operation": 6,
                    "source_of_finance": 7, "ownership": 8, "social_group": 9,
                    "establishments_in_household": 10, "nic_description": 11,
                    "handloom_activity": 12, "gender_code": 13, "religion_code": 14,
                    "hired_male_workers": 15, "hired_female_workers": 16,
                    "unpaid_male_workers": 17, "unpaid_female_workers": 18, "total_workers": 19,
                },
                2: {
                    "sl_no": 0, "state": 1, "sector": 2, "district": 3,
                    "activity": 4, "enterprise_classification": 5, "nature_of_operation": 6,
                    "ownership": 7, "source_of_finance": 8, "social_group": 9,
                    "power_fuel_usage": 10, "hired_male_workers": 11, "hired_female_workers": 12,
                    "male_child_workers": 13, "female_child_workers": 14,
                    "unpaid_male_child_workers": 15, "unpaid_female_child_workers": 16,
                    "unpaid_male_workers": 17, "unpaid_female_workers": 18, "total_workers": 19,
                    "registration_code1": 20, "registration_code2": 21,
                },
                3: {
                    "sl_no": 0, "state": 1, "sector": 2, "district": 3,
                    "activity": 4, "enterprise_classification": 5, "nature_of_operation": 6,
                    "ownership": 7, "source_of_finance": 8, "social_group": 9,
                    "power_fuel_usage": 10, "nic_description": 11,
                    "male_workers": 12, "female_workers": 13,
                    "male_child_workers": 14, "female_child_workers": 15,
                    "total_workers": 16, "enterprise_type": 17,
                },
            }
            col_map = col_maps.get(indicator_code, col_maps[1])

            rows = []
            html = raw.get("code", "")
            if html and "No Record" not in html:
                soup = BeautifulSoup(f"<table>{html}</table>", "html.parser")
                for row in soup.find_all("tr"):
                    cols = row.find_all("td")
                    if len(cols) >= 10:
                        row_data = {}
                        for field, idx in col_map.items():
                            row_data[field] = cols[idx].get_text(strip=True) if idx < len(cols) else ""
                        rows.append(row_data)

            total_records = int(str(raw.get("counter", 0) or 0).replace(",", ""))
            total_pages = math.ceil(total_records / 20) if total_records else 0

            return {
                "data": rows,
                "page": int(page_num),
                "total_pages": total_pages,
                "total_records": total_records,
                "statusCode": True,
            }
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}
