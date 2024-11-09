export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const pathName = url.pathname;
  const videoId = url.searchParams.get("video_id");

  // Check if the video_id query parameter is provided
  if (!videoId) {
    return new Response("Missing 'video_id' query parameter", { status: 400 });
  }

  // Construct the HLS manifest URL using the video ID
  const hlsStreamUrl = `https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1731206686/ei/vskvZ72ZGK6YsfIP5M7ZQA/ip/104.28.237.111/id/${videoId}.1/itag/234/source/yt_live_broadcast/requiressl/yes/ratebypass/yes/live/1/goi/133/sgoap/gir%3Dyes%3Bitag%3D140/rqh/1/hdlc/1/hls_chunk_host/rr4---sn-q4flrnsl.googlevideo.com/xpc/EgVo2aDSNQ%3D%3D/playlist_duration/3600/manifest_duration/3600/vprv/1/playlist_type/DVR/met/1731185087,/mh/SL/mm/44/mn/sn-q4flrnsl/ms/lva/mv/u/mvi/4/pl/27/rms/lva,lva/dover/13/pacing/0/short_key/1/keepalive/yes/fexp/51312688,51326932/mt/1731183568/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,live,goi,sgoap,rqh,hdlc,xpc,playlist_duration,manifest_duration,vprv,playlist_type/sig/AJfQdSswRAIgblDnvx-Vjc8wHq5WqjBtVn9EtDptcLlcliZJWUqRDPYCICeuEgew4pBvELVopKElH2THs7glOIIpxBvsAFCUEef7/lsparams/hls_chunk_host,met,mh,mm,mn,ms,mv,mvi,pl,rms/lsig/AGluJ3MwRAIgCzC9V3RCWZlxd6PbC5oUiD7sD8HRcX6WX5igRxwpeCICIFhxv5lSSUPH8ubZNzNXecKaUp8hvTaPCf23_FP4wrWL/playlist/index.m3u8`;

  // Redirect the user to the HLS stream URL
  return Response.redirect(hlsStreamUrl, 302);
}
