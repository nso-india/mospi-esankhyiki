{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# esankhyiki - Examples\n",
    "\n",
    "Python client for India's National Statistical Office (MoSPI) data portal.\n",
    "Access indicators across 22 datasets: employment, prices, GDP, health, education, environment, and more.\n",
    "\n",
    "```bash\n",
    "pip install mospi-esankhyiki[pandas]\n",
    "```"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "import esankhyiki\n",
    "from esankhyiki.exceptions import InvalidDatasetError, InvalidFilterError, APIError, NoDataError"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Available Datasets"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "esankhyiki.list_datasets(format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## PLFS - Periodic Labour Force Survey\n",
    "\n",
    "Covers labour force participation, unemployment, worker population ratio, wages.\n",
    "Use `get_indicators` to see what indicator codes are available, `get_metadata` to see valid filter values for a given indicator."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Indicators grouped by frequency_code\n",
    "indicators = esankhyiki.get_indicators(\"PLFS\")\n",
    "for group, items in indicators[\"indicators_by_frequency\"].items():\n",
    "    print(f\"\\n{group}:\")\n",
    "    for item in items:\n",
    "        print(f\"  {item['indicator_code']}: {item.get('indicator_name', item.get('description', ''))}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Valid filter values for Unemployment Rate (indicator_code=3), Annual (frequency_code=1)\n",
    "metadata = esankhyiki.get_metadata(\"PLFS\", indicator_code=3, frequency_code=1, year_type_code=1)\n",
    "for key, values in metadata[\"filter_values\"][\"data\"].items():\n",
    "    print(f\"\\n{key}:\")\n",
    "    for v in values[:4]:\n",
    "        print(f\"  {v}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Unemployment Rate - All India, all years, both sectors\n",
    "esankhyiki.get_data(\"PLFS\", {\n",
    "    \"indicator_code\": 3,\n",
    "    \"frequency_code\": 1,\n",
    "    \"year_type_code\":1,\n",
    "    \"state_code\": 99,     # 99 = All India\n",
    "    \"gender_code\": 3,     # 3 = Person\n",
    "    \"age_code\": 1,        # 1 = 15 years and above\n",
    "    \"sector_code\": 3,     # 3 = rural + urban\n",
    "}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## CPI - Consumer Price Index\n",
    "\n",
    "Multiple base years (2010, 2012, 2024) and two levels: Group and Item."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Available base years, levels, and series\n",
    "esankhyiki.get_indicators(\"CPI\", format=\"df\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Filter values for base_year=2012, Group level\n",
    "metadata = esankhyiki.get_metadata(\"CPI\", base_year=\"2012\", level=\"Group\", series=\"Current\", format=\"df\")\n",
    "metadata"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# CPI Group index, base year 2012, year 2024\n",
    "esankhyiki.get_data(\"CPI\", {\n",
    "    \"base_year\": \"2012\",\n",
    "    \"series\": \"Current\",\n",
    "    \"year\": \"2024\",\n",
    "}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## NAS - National Accounts Statistics (GDP)\n",
    "\n",
    "Annual and quarterly GDP, GVA, consumption, capital formation by industry and institutional sector."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "esankhyiki.get_indicators(\"NAS\", format=\"df\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Filter values for GVA by industry (indicator_code=1), base year 2022-23\n",
    "metadata = esankhyiki.get_metadata(\"NAS\", indicator_code=1, base_year=\"2022-23\", series=\"Current\", frequency_code=1)\n",
    "for key, values in metadata.items():\n",
    "    if isinstance(values, list):\n",
    "        print(f\"{key}: {values[:3]}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# GVA by industry, current prices, latest estimates\n",
    "esankhyiki.get_data(\"NAS\", {\n",
    "    \"indicator_code\": 1,\n",
    "    \"base_year\": \"2022-23\",\n",
    "    \"series\": \"Current\",\n",
    "    \"frequency_code\": 1,\n",
    "    \"year\": \"2024-25\",\n",
    "}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## IIP - Index of Industrial Production\n",
    "\n",
    "Monthly and annual industrial output across manufacturing, mining, and electricity sectors."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Available categories and years for IIP annual\n",
    "metadata = esankhyiki.get_metadata(\"IIP\", base_year=\"2011-12\", frequency=\"Annually\")\n",
    "metadata"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# IIP annual, 2023-24\n",
    "esankhyiki.get_data(\"IIP\", {\n",
    "    \"base_year\": \"2011-12\",\n",
    "    \"financial_year\": \"2023-24\",\n",
    "}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## GENDER - Gender Statistics\n",
    "\n",
    "147 indicators covering demographics, health, education, labour, financial inclusion, and crimes against women."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "indicators = esankhyiki.get_indicators(\"GENDER\")\n",
    "print(f\"Total indicators: {len(indicators)}\\n\")\n",
    "for i in indicators[:10]:\n",
    "    print(f\"  {i['indicator_code']}: {i['description']}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Sex ratio (indicator_code=2)\n",
    "esankhyiki.get_data(\"GENDER\", {\"indicator_code\": 2}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## ENVSTATS - Environment Statistics\n",
    "\n",
    "124 indicators covering climate, water, forests, biodiversity, pollution, and natural disasters."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "indicators = esankhyiki.get_indicators(\"ENVSTATS\")\n",
    "print(f\"Total indicators: {len(indicators)}\\n\")\n",
    "for i in indicators[:10]:\n",
    "    print(f\"  {i['indicator_code']}: {i.get('description', i.get('label', ''))}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Mean temperature trend (indicator_code=1)\n",
    "esankhyiki.get_data(\"ENVSTATS\", {\"indicator_code\": 1}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## RBI - Foreign Trade and Exchange Rates\n",
    "\n",
    "39 indicators on balance of payments, forex reserves, exchange rates (155 currencies), NRI deposits."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "indicators = esankhyiki.get_indicators(\"RBI\")\n",
    "for i in indicators:\n",
    "    print(f\"  {i['indicator_code']}: {i['label']}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Get valid sub_indicator_codes for Balance of Payments (indicator_code=22)\n",
    "metadata = esankhyiki.get_metadata(\"RBI\", sub_indicator_code=22)\n",
    "metadata"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Balance of Payments\n",
    "esankhyiki.get_data(\"RBI\", {\"indicator_code\": 22}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## EC - Economic Census\n",
    "\n",
    "District-level establishment and worker counts across three census editions (EC4/EC5/EC6)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "esankhyiki.get_indicators(\"EC\", format=\"df\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# EC6 (2013-14) - available states and filter options\n",
    "metadata = esankhyiki.get_metadata(\"EC\", indicator_code=1)\n",
    "metadata"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# EC6 - top districts in Maharashtra by establishments\n",
    "esankhyiki.get_data(\"EC\", {\n",
    "    \"indicator_code\": 1,\n",
    "    \"state\": \"27\",       # Maharashtra\n",
    "    \"mode\": \"ranking\",\n",
    "    \"top5opt\": \"2\",\n",
    "}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## MNRE - Renewable Energy\n",
    "\n",
    "State-wise monthly installed capacity (in MW) for solar, wind, hydro, bio, and total renewable power from the Ministry of New and Renewable Energy."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>type_of_renewable_energy_code</th>\n",
       "      <th>label</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>Solar Power</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>Wind Power</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>Hydro Power</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>Bio Power</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>Total Power</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   type_of_renewable_energy_code        label\n",
       "0                              1  Solar Power\n",
       "1                              2   Wind Power\n",
       "2                              3  Hydro Power\n",
       "3                              4    Bio Power\n",
       "4                              5  Total Power"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Energy types: 1=Solar, 2=Wind, 3=Hydro, 4=Bio, 5=Total\n",
    "# Solar/Hydro/Bio support category_code breakdown; Wind and Total do not\n",
    "esankhyiki.get_indicators(\"MNRE\", format=\"df\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'year': [{'year': 2026},\n",
       "   {'year': 2025},\n",
       "   {'year': 2024},\n",
       "   {'year': 2023},\n",
       "   {'year': 2022},\n",
       "   {'year': 2021},\n",
       "   {'year': 2020}],\n",
       "  'month': [{'month_code': 12, 'label': 'December'},\n",
       "   {'month_code': 11, 'label': 'November'},\n",
       "   {'month_code': 10, 'label': 'October'},\n",
       "   {'month_code': 9, 'label': 'September'},\n",
       "   {'month_code': 8, 'label': 'August'},\n",
       "   {'month_code': 7, 'label': 'July'},\n",
       "   {'month_code': 6, 'label': 'June'},\n",
       "   {'month_code': 5, 'label': 'May'},\n",
       "   {'month_code': 4, 'label': 'April'},\n",
       "   {'month_code': 3, 'label': 'March'},\n",
       "   {'month_code': 2, 'label': 'February'},\n",
       "   {'month_code': 1, 'label': 'January'}],\n",
       "  'state': [{'state_code': 36, 'label': 'All India'},\n",
       "   {'state_code': 39, 'label': 'Andaman and Nicobar Islands'},\n",
       "   {'state_code': 1, 'label': 'Andhra Pradesh'},\n",
       "   {'state_code': 2, 'label': 'Arunachal Pradesh'},\n",
       "   {'state_code': 3, 'label': 'Assam'},\n",
       "   {'state_code': 4, 'label': 'Bihar'},\n",
       "   {'state_code': 30, 'label': 'Chandigarh'},\n",
       "   {'state_code': 5, 'label': 'Chhattisgarh'},\n",
       "   {'state_code': 37, 'label': 'Dadar and Nagar Haveli'},\n",
       "   {'state_code': 31, 'label': 'Dadra & Nagar Haveli and Daman & Diu'},\n",
       "   {'state_code': 38, 'label': 'Daman and Diu'},\n",
       "   {'state_code': 6, 'label': 'Delhi'},\n",
       "   {'state_code': 7, 'label': 'Goa'},\n",
       "   {'state_code': 8, 'label': 'Gujarat'},\n",
       "   {'state_code': 9, 'label': 'Haryana'},\n",
       "   {'state_code': 10, 'label': 'Himachal Pradesh'},\n",
       "   {'state_code': 32, 'label': 'Jammu and Kashmir'},\n",
       "   {'state_code': 11, 'label': 'Jharkhand'},\n",
       "   {'state_code': 12, 'label': 'Karnataka'},\n",
       "   {'state_code': 13, 'label': 'Kerala'},\n",
       "   {'state_code': 33, 'label': 'Ladakh'},\n",
       "   {'state_code': 34, 'label': 'Lakshadweep'},\n",
       "   {'state_code': 14, 'label': 'Madhya Pradesh'},\n",
       "   {'state_code': 15, 'label': 'Maharashtra'},\n",
       "   {'state_code': 16, 'label': 'Manipur'},\n",
       "   {'state_code': 17, 'label': 'Meghalaya'},\n",
       "   {'state_code': 18, 'label': 'Mizoram'},\n",
       "   {'state_code': 19, 'label': 'Nagaland'},\n",
       "   {'state_code': 20, 'label': 'Odisha'},\n",
       "   {'state_code': 40, 'label': 'Others'},\n",
       "   {'state_code': 35, 'label': 'Puducherry'},\n",
       "   {'state_code': 21, 'label': 'Punjab'},\n",
       "   {'state_code': 22, 'label': 'Rajasthan'},\n",
       "   {'state_code': 23, 'label': 'Sikkim'},\n",
       "   {'state_code': 24, 'label': 'Tamil Nadu'},\n",
       "   {'state_code': 25, 'label': 'Telangana'},\n",
       "   {'state_code': 26, 'label': 'Tripura'},\n",
       "   {'state_code': 28, 'label': 'Uttarakhand'},\n",
       "   {'state_code': 27, 'label': 'Uttar Pradesh'},\n",
       "   {'state_code': 29, 'label': 'West Bengal'}],\n",
       "  'category': [{'category_code': 1,\n",
       "    'label': 'Ground Mounted Solar Power',\n",
       "    'type_of_renewable_energy_code': 1},\n",
       "   {'category_code': 2,\n",
       "    'label': 'Rooftop Solar Power',\n",
       "    'type_of_renewable_energy_code': 1},\n",
       "   {'category_code': 3,\n",
       "    'label': ' Hybrid Solar Component',\n",
       "    'type_of_renewable_energy_code': 1},\n",
       "   {'category_code': 4,\n",
       "    'label': 'Off-Grid Solar Power/KUSUM',\n",
       "    'type_of_renewable_energy_code': 1},\n",
       "   {'category_code': 5,\n",
       "    'label': 'Solar Power Total',\n",
       "    'type_of_renewable_energy_code': 1}]}]"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Filter values for Solar Power (type 1) - returns valid category_codes\n",
    "metadata = esankhyiki.get_metadata(\"MNRE\", indicator_code=1)\n",
    "metadata"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>type_of_renewable_energy</th>\n",
       "      <th>year</th>\n",
       "      <th>month</th>\n",
       "      <th>state</th>\n",
       "      <th>category</th>\n",
       "      <th>value</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>December</td>\n",
       "      <td>All India</td>\n",
       "      <td>Ground Mounted Solar Power</td>\n",
       "      <td>56920.20</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>December</td>\n",
       "      <td>All India</td>\n",
       "      <td>Rooftop Solar Power</td>\n",
       "      <td>11078.94</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>December</td>\n",
       "      <td>All India</td>\n",
       "      <td>Hybrid Solar Component</td>\n",
       "      <td>2571.96</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>December</td>\n",
       "      <td>All India</td>\n",
       "      <td>Off-Grid Solar Power/KUSUM</td>\n",
       "      <td>2748.39</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>December</td>\n",
       "      <td>All India</td>\n",
       "      <td>Solar Power Total</td>\n",
       "      <td>73319.50</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>November</td>\n",
       "      <td>All India</td>\n",
       "      <td>Ground Mounted Solar Power</td>\n",
       "      <td>55958.18</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>November</td>\n",
       "      <td>All India</td>\n",
       "      <td>Rooftop Solar Power</td>\n",
       "      <td>11078.94</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>November</td>\n",
       "      <td>All India</td>\n",
       "      <td>Hybrid Solar Component</td>\n",
       "      <td>2570.96</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>November</td>\n",
       "      <td>All India</td>\n",
       "      <td>Off-Grid Solar Power/KUSUM</td>\n",
       "      <td>2703.53</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>Solar Power</td>\n",
       "      <td>2023</td>\n",
       "      <td>November</td>\n",
       "      <td>All India</td>\n",
       "      <td>Solar Power Total</td>\n",
       "      <td>72311.62</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  type_of_renewable_energy  year     month      state  \\\n",
       "0              Solar Power  2023  December  All India   \n",
       "1              Solar Power  2023  December  All India   \n",
       "2              Solar Power  2023  December  All India   \n",
       "3              Solar Power  2023  December  All India   \n",
       "4              Solar Power  2023  December  All India   \n",
       "5              Solar Power  2023  November  All India   \n",
       "6              Solar Power  2023  November  All India   \n",
       "7              Solar Power  2023  November  All India   \n",
       "8              Solar Power  2023  November  All India   \n",
       "9              Solar Power  2023  November  All India   \n",
       "\n",
       "                     category     value  \n",
       "0  Ground Mounted Solar Power  56920.20  \n",
       "1         Rooftop Solar Power  11078.94  \n",
       "2      Hybrid Solar Component   2571.96  \n",
       "3  Off-Grid Solar Power/KUSUM   2748.39  \n",
       "4           Solar Power Total  73319.50  \n",
       "5  Ground Mounted Solar Power  55958.18  \n",
       "6         Rooftop Solar Power  11078.94  \n",
       "7      Hybrid Solar Component   2570.96  \n",
       "8  Off-Grid Solar Power/KUSUM   2703.53  \n",
       "9           Solar Power Total  72311.62  "
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "esankhyiki.get_data(\"MNRE\", {\n",
    "    \"type_of_renewable_energy_code\": 1,  # Solar Power\n",
    "    \"state_code\": 36,                    # All India\n",
    "    \"year\": \"2023\",\n",
    "}, format=\"df\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Output Formats\n",
    "\n",
    "All functions support `format=\"dict\"` (default), `format=\"df\"` (pandas DataFrame), or `format=\"csv\"`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "csv_str = esankhyiki.get_data(\"PLFS\", {\n",
    "    \"indicator_code\": 3,\n",
    "    \"frequency_code\": 1,\n",
    "    \"year_type_code\":1,\n",
    "    \"year\": \"2023-24\",\n",
    "    \"state_code\": 99,\n",
    "    \"gender_code\": 3,\n",
    "    \"age_code\": 1,\n",
    "    \"sector_code\": 3,\n",
    "}, format=\"csv\")\n",
    "\n",
    "print(csv_str[:600])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Error Handling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Typo in dataset name - fuzzy suggestion\n",
    "try:\n",
    "    esankhyiki.get_indicators(\"plfs_data\")\n",
    "except InvalidDatasetError as e:\n",
    "    print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Missing required parameter\n",
    "try:\n",
    "    esankhyiki.get_metadata(\"PLFS\", frequency_code=1)\n",
    "except InvalidFilterError as e:\n",
    "    print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Invalid filter parameter name\n",
    "try:\n",
    "    esankhyiki.get_data(\"PLFS\", {\n",
    "        \"indicator_code\": 1,\n",
    "        \"frequency_code\": 1,\n",
    "        \"typo_param\": \"hello\",\n",
    "    })\n",
    "except InvalidFilterError as e:\n",
    "    print(e)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
