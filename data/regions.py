"""
Single source of truth for which cloud regions the GreenGPU Explorer
compares, and their country (used to join real grid carbon-intensity
data) and location label (for display).

Regions were chosen because AWS actually offers at least one of our
target GPU models (L40S, A100-80GB, H100) there, per the public
SkyPilot cloud-instance catalog (see fetch_gpu_pricing.py) -- these
aren't arbitrary city names, they're real AWS region codes.

`diurnal_swing_pct` and `grid_mix_note` are editorial/illustrative
fallbacks, used to shape a synthetic hourly curve when no live feed is
available; `country` feeds a real published annual-average carbon
intensity figure via fetch_carbon_intensity.py.

`electricitymaps_zone` is this region's approximate Electricity Maps
zone key (https://api.electricitymap.org/v3), used by
scheduler/live_carbon.py when an API key is configured. These mappings
are a best-effort guess at the right zone for each AWS region (several
countries have multiple sub-national zones and AWS doesn't publish which
grid/substation actually feeds a given data center) -- they have NOT been
validated against a real API response with a real key yet (the host only
became reachable from this build environment partway through the
project; a real (unauthenticated) request confirmed it responds, but no
key was available to check the payload shape). Treat them as a starting
point to verify, not a certified mapping.

`uk_carbon_intensity_regionid` is a real, *verified* regionid from the
UK's free/no-auth Carbon Intensity API (see scheduler/live_carbon_uk.py)
-- only set for eu-west-2 (London), the one region this API covers.
Confirmed by listing /regional and matching by shortname ("London").
"""

REGIONS = [
    {"region": "us-east-1", "cloud": "AWS", "location": "N. Virginia, United States", "country": "United States", "diurnal_swing_pct": 25, "grid_mix_note": "Gas + coal mix", "electricitymaps_zone": "US-MIDA-PJM"},
    {"region": "us-east-2", "cloud": "AWS", "location": "Ohio, United States", "country": "United States", "diurnal_swing_pct": 25, "grid_mix_note": "Gas + coal mix", "electricitymaps_zone": "US-MIDA-PJM"},
    {"region": "us-west-1", "cloud": "AWS", "location": "N. California, United States", "country": "United States", "diurnal_swing_pct": 30, "grid_mix_note": "Mixed, more renewables regionally", "electricitymaps_zone": "US-CAL-CISO"},
    {"region": "us-west-2", "cloud": "AWS", "location": "Oregon, United States", "country": "United States", "diurnal_swing_pct": 30, "grid_mix_note": "Mixed with growing wind/solar/hydro", "electricitymaps_zone": "US-NW-BPAT"},
    {"region": "ca-central-1", "cloud": "AWS", "location": "Montreal, Canada", "country": "Canada", "diurnal_swing_pct": 20, "grid_mix_note": "Hydro + nuclear, some fossil provinces", "electricitymaps_zone": "CA-QC"},
    {"region": "eu-west-2", "cloud": "AWS", "location": "London, United Kingdom", "country": "United Kingdom", "diurnal_swing_pct": 30, "grid_mix_note": "Gas + wind mix", "electricitymaps_zone": "GB", "uk_carbon_intensity_regionid": 13},
    {"region": "eu-central-1", "cloud": "AWS", "location": "Frankfurt, Germany", "country": "Germany", "diurnal_swing_pct": 30, "grid_mix_note": "Coal + wind mix", "electricitymaps_zone": "DE"},
    {"region": "eu-north-1", "cloud": "AWS", "location": "Stockholm, Sweden", "country": "Sweden", "diurnal_swing_pct": 20, "grid_mix_note": "Hydro + nuclear dominant", "electricitymaps_zone": "SE-SE3"},
    {"region": "eu-south-2", "cloud": "AWS", "location": "Zaragoza, Spain", "country": "Spain", "diurnal_swing_pct": 25, "grid_mix_note": "Wind + gas mix", "electricitymaps_zone": "ES"},
    {"region": "me-central-1", "cloud": "AWS", "location": "United Arab Emirates", "country": "United Arab Emirates", "diurnal_swing_pct": 15, "grid_mix_note": "Gas dominant", "electricitymaps_zone": "AE"},
    {"region": "ap-northeast-1", "cloud": "AWS", "location": "Tokyo, Japan", "country": "Japan", "diurnal_swing_pct": 20, "grid_mix_note": "Gas + coal mix", "electricitymaps_zone": "JP-TK"},
    {"region": "ap-northeast-2", "cloud": "AWS", "location": "Seoul, South Korea", "country": "South Korea", "diurnal_swing_pct": 20, "grid_mix_note": "Coal + gas mix", "electricitymaps_zone": "KR"},
    {"region": "ap-northeast-3", "cloud": "AWS", "location": "Osaka, Japan", "country": "Japan", "diurnal_swing_pct": 20, "grid_mix_note": "Gas + coal mix", "electricitymaps_zone": "JP-KN"},
    {"region": "ap-south-1", "cloud": "AWS", "location": "Mumbai, India", "country": "India", "diurnal_swing_pct": 20, "grid_mix_note": "Coal dominant", "electricitymaps_zone": "IN-WE"},
    {"region": "ap-southeast-1", "cloud": "AWS", "location": "Singapore", "country": "Singapore", "diurnal_swing_pct": 15, "grid_mix_note": "Gas dominant", "electricitymaps_zone": "SG"},
    {"region": "ap-southeast-2", "cloud": "AWS", "location": "Sydney, Australia", "country": "Australia", "diurnal_swing_pct": 25, "grid_mix_note": "Coal dominant", "electricitymaps_zone": "AU-NSW"},
    {"region": "ap-southeast-3", "cloud": "AWS", "location": "Jakarta, Indonesia", "country": "Indonesia", "diurnal_swing_pct": 15, "grid_mix_note": "Coal dominant", "electricitymaps_zone": "ID"},
]
