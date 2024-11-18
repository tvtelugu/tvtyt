export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const pathName = url.pathname;
  const channelId = url.searchParams.get("channel_id");
  const videoId = url.searchParams.get("video_id");

  if (!channelId && !videoId) {
    console.log("Error: Missing 'channel_id' or 'video_id' query parameter");
    return new Response("Missing 'channel_id' or 'video_id' query parameter", { status: 400 });
  }

  const youtubeUrl = videoId
    ? `https://www.youtube.com/watch?v=${videoId}`
    : `https://www.youtube.com/channel/${channelId}/live`;

  async function dashUrl(ytUrl) {
    try {
      const response = await fetch(ytUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
      const text = await response.text();
      const match = text.match(/(?<=dashManifestUrl":").+?(?=",)/g);
      return match ? match[0] : null;
    } catch (err) {
      console.log("Error in dashUrl function:", err);
      return null;
    }
  }

  async function hlsUrl(ytUrl) {
    try {
      const response = await fetch(ytUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
      const text = await response.text();
      const match = text.match(/(?<=hlsManifestUrl":").*\.m3u8/g);
      return match ? match[0] : null;
    } catch (err) {
      console.log("Error in hlsUrl function:", err);
      return null;
    }
  }

  switch (pathName) {
    case "/master.mpd":
      try {
        console.log(`Fetching DASH URL for ${youtubeUrl}`);
        const dashUrlResponse = await dashUrl(youtubeUrl);
        if (dashUrlResponse) {
          console.log(`Redirecting to DASH URL: ${dashUrlResponse}`);
          return Response.redirect(dashUrlResponse, 302);
        } else {
          console.log("dashManifestUrl not found in response.");
          return new Response("dashManifestUrl not found", { status: 404 });
        }
      } catch (err) {
        console.log("Error in DASH URL fetch:", err);
        return new Response("Error fetching DASH manifest URL", { status: 500 });
      }

    case "/master.m3u8":
      try {
        console.log(`Fetching HLS URL for ${youtubeUrl}`);
        const hlsUrlResponse = await hlsUrl(youtubeUrl);
        if (hlsUrlResponse) {
          console.log(`Redirecting to HLS URL: ${hlsUrlResponse}`);
          return Response.redirect(hlsUrlResponse, 302);
        } else {
          console.log("hlsManifestUrl not found in response.");
          return new Response("hlsManifestUrl not found", { status: 404 });
        }
      } catch (err) {
        console.log("Error in HLS URL fetch:", err);
        return new Response("Error fetching HLS manifest URL", { status: 500 });
      }

    default:
      console.log("Error: Invalid path. Use /master.mpd or /master.m3u8");
      return new Response("Invalid path. Use /master.mpd or /master.m3u8", { status: 400 });
  }
}
