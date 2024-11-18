export async function onRequest({ request }) {
  const url = new URL(request.url);
  const channelId = url.searchParams.get('id'); // Get the channel ID from the query parameter

  if (!channelId) {
    return new Response('Channel ID not provided in query parameter "id".', { status: 400 });
  }

  try {
    const streamUrl = await getStream(channelId);
    if (streamUrl) {
      return Response.redirect(streamUrl, 302);  // Redirect to the live stream
    } else {
      return new Response('Live stream not found for the provided channel.', { status: 404 });
    }
  } catch (err) {
    return new Response('Error fetching the live stream: ' + err.message, { status: 500 });
  }
}

async function getStream(id) {
  let url = 'https://www.youtube.com/channel/' + id + '/live';
  const { body } = await fetch(url);  // Make a request to the YouTube live URL
  let bodyText = await body.text();
  let stream = bodyText.match(/(?<=hlsManifestUrl":").*\.m3u8/g);  // Match the stream URL
  if (stream) {
    return stream[0];  // Return the first stream URL
  } else {
    return null;  // No stream found
  }
}
