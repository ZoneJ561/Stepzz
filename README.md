# StepDaddyLiveHD

A self-hosted IPTV helper built with [Reflex](https://reflex.dev). StepDaddyLiveHD keeps an up-to-date catalogue of channels from DaddyLive, exposes a downloadable `playlist.m3u8`, and offers a searchable schedule to see what is on right now. To prevent the playlist from being shared publicly you can lock it behind a shared secret code so only trusted viewers can access the download link.

## Features

- **Channel Directory**: Browse and search the full DaddyLive line-up with artwork and tags.
- **Event Schedule**: Filter the programme guide to quickly find upcoming events across categories.
- **Secret-Gated Playlist**: Require a shared secret code before revealing the `playlist.m3u8` download link.
- **Customizable Hosting**: Run locally or via Docker with optional SOCKS5 and proxy configuration.

---

## Installation

### Local Installation

1. Install Python (tested with version 3.12).
2. Clone the repository and navigate to the project directory.
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Initialize Reflex:
   ```bash
   reflex init
   ```
6. Run the application in production mode:
   ```bash
   reflex run --env prod
   ```

### Docker Installation

1. Docker Installation:
   ```bash
   docker build -t step-daddy-live-hd .
   ```
2. Run the container:
   ```bash
   docker run -p 3000:3000 step-daddy-live-hd
   ```

---

## Configuration

### Environment Variables
- **PLAYLIST_SECRET_CODE**: Secret phrase required to unlock and download `playlist.m3u8`. Leave empty to make the playlist public.
- **PORT**: Specify a custom port for the application.
- **API_URL**: Set the domain for hosting behind a custom domain.
- **SOCKS5**: Proxy requests to DLHD through your server.
- **PROXY_CONTENT**: Proxy the content/streams through your server.

### Example Docker Command
   ```bash
   docker build --build-arg PLAYLIST_SECRET_CODE=my-secret --build-arg PROXY_CONTENT=FALSE --build-arg API_URL=https://example.com --build-arg SOCKS5=user:password@proxy.example.com:1080 -t step-daddy-live-hd .
   docker run -e PLAYLIST_SECRET_CODE=my-secret -e PROXY_CONTENT=FALSE -e API_URL=https://example.com -e SOCKS5=user:password@proxy.example.com:1080 -p 3000:3000 step-daddy-live-hd
   ```

---

## Unlocking the Playlist

1. Set the `PLAYLIST_SECRET_CODE` environment variable (or build argument when using Docker) to the secret phrase you want to share with trusted viewers.
2. Start the application and visit `/playlist`.
3. Enter the shared code to reveal the download and copy controls for `playlist.m3u8`.
4. Share the full secret-scoped URL (e.g. `https://example.com/SECRET/playlist.m3u8`) only with users who should have access.

If the environment variable is omitted the playlist remains public and the `/playlist` page immediately exposes the download link.

---

## Site Map

### Pages

1. **Home**: Browse and search for TV channels.
2. **Schedule**: Filter the upcoming events guide.
3. **Playlist Access**: Unlock and download the `playlist.m3u8` file for integration with media players.

---

## Hosting Options
Refer to the [Reflex documentation](https://reflex.dev/docs/hosting/self-hosting/) for additional self-hosting methods.
