# vMix Scoreboard

Drive vMix title graphics from a physical scoreboard with a simple, scriptable bridge.

This project has two parts:
- `vMixIntegration.py`: Handles all API calls to vMix. It reads target details from config.JSON and pushes live scoreboard data to that target.
- `vMixScoreboard.py`: Implements the physical interface to the scoreboard hardware. Based on a command-line argument specifying the scoreboard model/protocol, it configures how data is read, then forwards that data to vMix via vMixIntegration.

## How it works
- `vMixScoreboard.py` connects to the specified scoreboard and continuously pulls live values (e.g., scores, clocks).
- `vMixIntegration.py` reads target info from `config.JSON` and updates the specified vMix title/input fields.
- The script runs on the hardware connected to the scoreboard or on a machine that can access it.

## Prerequisites
- vMix with the Web Controller/API enabled and reachable from the machine running the script.
- Access to the physical scoreboard or its data feed.
- A `config.JSON` file containing the vMix target information.

## Configuration (`config.JSON`)
Use `config.JSON` to point to the vMix system and map scoreboard values to the exact field names in your vMix title.

Example:
```json
{
    "vMix":[
        {
                "ip_adres":"10.12.0.60:8088",
                "vmix_id":"4e64175f-2b61-4edc-92c2-b60a836effc8",
                "score_home":"scoreHome.Text",
                "score_guest":"scoreAway.Text",
                "time_seconds":"timeSeconds.Text",
                "time_minutes":"timeMinutes.Text",
                "time_spacer":"timeSep.Text",
                "shotclock_seconds":"shotclock.Text"
        }
    ]
}
```

### Field details:
- `ip_adres`: The IP adress of the target device running vMix. Port `8088` specifies the port on which the vMix API is normally accessable.
- `vmix_id`: The ID of the vMix element (input/title) to update. Obtain this from `http://<ip_adress>:8088/API` (replace with the same IP as ip_adress).
- `score_home`, `score_guest`, and any additional fields: Set each value to the exact field name in the target title of the specified `vmix_id`.

## Usage
Example CLI:

```powershell
python vMixScoreboard.py -m <DataDisplay, AnatecIndor> -j vMixConfig.JSON -c tty/dev0
```

## Troubleshooting
- Connection issues: verify ip_adress is reachable and vMix API is enabled.
- Wrong target: confirm vmix_id by visiting http://<ip_adress>:8088/API and matching the input/title ID.
- No updates: ensure every mapped field (e.g., score_home, score_guest, etc.) matches the exact field names in the vMix title.

## vMix API
This project uses the vMix Developer API to update titles and fields from the Raspberry Pi. Documentation: https://www.vmix.com/help19/index.htm?DeveloperAPI.html