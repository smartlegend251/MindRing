// Initialize Cast SDK
window['__onGCastApiAvailable'] = function(isAvailable) {
    if (isAvailable) {
      initializeCastApi();
    }
  };
  
  // Initialize Cast API
  function initializeCastApi() {
    const applicationId = 'YOUR_APPLICATION_ID'; // Replace with your Chromecast application ID
  
    // Load the Cast API
    cast.framework.CastContext.getInstance().setOptions({
      receiverApplicationId: applicationId,
      autoJoinPolicy: chrome.cast.AutoJoinPolicy.ORIGIN_SCOPED
    });
  
    // Add event listener for Cast state changes
    cast.framework.CastContext.getInstance().addEventListener(
      cast.framework.CastContextEventType.SESSION_STATE_CHANGED,
      onSessionStateChanged
    );
  }
  
  // Handle Cast state changes
  function onSessionStateChanged(event) {
    if (event.sessionState === cast.framework.SessionState.SESSION_STARTED) {
      // Cast session started
      console.log('Casting started');
    } else if (
      event.sessionState === cast.framework.SessionState.SESSION_ENDED ||
      event.sessionState === cast.framework.SessionState.SESSION_ERROR
    ) {
      // Cast session ended or encountered an error
      console.log('Casting ended');
    }
  }
  
  // Start casting
  function startCasting() {
    const mediaInfo = new chrome.cast.media.MediaInfo('VIDEO_URL', 'video/mp4');
    const request = new chrome.cast.media.LoadRequest(mediaInfo);
  
    cast.framework.CastContext.getInstance().getCurrentSession().loadMedia(request);
  }
  
  // Add click event listener to the Cast button
  const castButton = document.getElementById('cast-button');
  castButton.addEventListener('click', startCasting);
  