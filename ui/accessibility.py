import html
import streamlit.components.v1 as components

def listen_to_text(text: str, key: str = "voice_player"):
    safe = html.escape(text).replace("\n", "<br>")
    component = f"""
    <div style="font-family:system-ui,sans-serif;border:1px solid #e5e7eb;border-radius:12px;padding:12px;background:#fff">
      <button id="play-{key}" aria-label="Listen to generated draft" style="border:1px solid #d1d5db;border-radius:9px;background:#111827;color:white;padding:9px 14px;font-weight:650;cursor:pointer">▶ Listen to draft</button>
      <button id="stop-{key}" aria-label="Stop audio playback" style="border:1px solid #d1d5db;border-radius:9px;background:white;color:#111827;padding:9px 14px;font-weight:650;cursor:pointer">■ Stop</button>
      <label for="rate-{key}" style="font-size:13px;color:#475569;margin-left:8px">Speed</label>
      <select id="rate-{key}" aria-label="Speech speed"><option value="0.85">0.85×</option><option value="1" selected>1×</option><option value="1.15">1.15×</option></select>
      <p id="status-{key}" aria-live="polite" style="margin:8px 0 0;color:#64748b;font-size:12px">Uses your browser's built-in speech engine. No audio API key required.</p>
      <div style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden">{safe}</div>
    </div>
    <script>
      const text = {text!r};
      const play = document.getElementById('play-{key}'), stop = document.getElementById('stop-{key}');
      const rate = document.getElementById('rate-{key}'), status = document.getElementById('status-{key}');
      function stopSpeech() {{ window.speechSynthesis.cancel(); status.textContent='Playback stopped.'; }}
      play.addEventListener('click', () => {{
        if (!('speechSynthesis' in window)) {{ status.textContent='Speech playback is not supported by this browser.'; return; }}
        stopSpeech(); const u=new SpeechSynthesisUtterance(text); u.rate=Number(rate.value);
        u.onstart=()=>status.textContent='Playing…'; u.onend=()=>status.textContent='Finished. Press Listen to play again.';
        u.onerror=()=>status.textContent='Could not play this draft. Check browser audio permissions.';
        window.speechSynthesis.speak(u);
      }});
      stop.addEventListener('click', stopSpeech);
    </script>
    """
    components.html(component, height=108)
