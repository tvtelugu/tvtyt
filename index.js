<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>YouTube Live Stream</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
    input { padding: 10px; width: 250px; }
    button { padding: 10px; width: 150px; margin-top: 10px; }
  </style>
</head>
<body>
  <h1>Enter YouTube Channel ID for Live Stream</h1>
  <input type="text" id="channelId" placeholder="Enter Channel ID" />
  <button onclick="redirectToStream()">Go Live</button>

  <script>
    function redirectToStream() {
      const channelId = document.getElementById('channelId').value.trim();
      if (channelId) {
        window.location.href = `https://tvtyt.pages.dev/play.m3u8?id=${channelId}`;
      } else {
        alert('Please enter a channel ID');
      }
    }
  </script>
</body>
</html>
