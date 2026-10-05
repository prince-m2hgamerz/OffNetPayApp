const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

// ─── Tab Switching ───
$$('.np-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('.np-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const tab = btn.dataset.tab;
    $('#pay-view').style.display    = tab === 'pay' ? 'block' : 'none';
    $('#scan-view').style.display   = tab === 'scan' ? 'block' : 'none';
    $('#bal-view').style.display    = tab === 'balance' ? 'block' : 'none';
    $('#history-view').style.display = tab === 'history' ? 'block' : 'none';
    $('#result-view').style.display = 'none';
    
    if (tab === 'history') {
      loadHistory();
    }

    if (tab === 'scan') {
      $('#qr-result').style.display = 'none';
      $('#qr-reader').style.display = 'block';
      if (typeof Html5Qrcode !== 'undefined') startQrScanner();
    } else {
      if (typeof Html5Qrcode !== 'undefined') stopQrScanner();
    }
  });
});

// ─── Amount Chips ───
$$('.amt-preset').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('.amt-preset').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    $('#amount').value = btn.dataset.amt;
    validatePay();
  });
});

// ─── Validation ───
const isValidVPA = vpa => /^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+$/.test(vpa.trim());
const isValidAmount = amt => { const n = parseFloat(amt); return !isNaN(n) && n >= 1 && n <= 100000; };

function validatePay() {
  const vpa = $('#vpa');
  const amt = $('#amount');
  const valid = vpa && amt && isValidVPA(vpa.value) && isValidAmount(amt.value);
  if ($('#pay-btn')) {
    $('#pay-btn').disabled = !valid;
  }
  return valid;
}

if ($('#vpa')) {
  $('#vpa').addEventListener('input', validatePay);
}
if ($('#amount')) {
  $('#amount').addEventListener('input', () => {
    $$('.amt-preset').forEach(b => b.classList.remove('active'));
    validatePay();
  });
}

// ─── Pay Action ───
if ($('#pay-btn')) {
  $('#pay-btn').addEventListener('click', () => {
    if (!validatePay()) return;
    const vpa = $('#vpa').value.trim();
    const amt = $('#amount').value.trim();

    saveToHistory(vpa);
    copyText(vpa);
    
    $('#pay-view').style.display = 'none';
    $('#result-view').style.display = 'block';
    $('#res-vpa').textContent = vpa;
    $('#res-amt').textContent = '₹' + amt;
  });
}

// ─── Helpers ───
function copyText(text) {
  navigator.clipboard.writeText(text).catch(() => {
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
  });
}

if ($('#copy-again-btn')) {
  $('#copy-again-btn').addEventListener('click', (e) => {
    copyText($('#res-vpa').textContent);
    const orig = e.target.textContent;
    e.target.textContent = '✅ Copied!';
    setTimeout(() => { e.target.textContent = orig; }, 1500);
  });
}

if ($('#reset-btn')) {
  $('#reset-btn').addEventListener('click', () => {
    $('#result-view').style.display = 'none';
    $('#pay-view').style.display = 'block';
  });
}

if ($('#bal-btn')) {
  $('#bal-btn').addEventListener('click', () => {
    window.location.href = "tel:*99*1*6%23";
  });
}

// ─── PWA Install Prompt ───
let deferredPrompt = null;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  if ($('#install-banner')) {
    $('#install-banner').style.display = 'block';
  }
});

if ($('#install-banner')) {
  $('#install-banner').addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    deferredPrompt = null;
    $('#install-banner').style.display = 'none';
  });
}

// ─── Service Worker ───
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js', { scope: './' }).catch(() => {});
}

// ─── History Logic ───
function saveToHistory(vpa) {
  let history = JSON.parse(localStorage.getItem('offnetpay_history') || '[]');
  history = history.filter(item => item !== vpa); // Remove duplicate
  history.unshift(vpa); // Add to top
  if (history.length > 10) history.pop(); // Keep only last 10
  localStorage.setItem('offnetpay_history', JSON.stringify(history));
}

function loadHistory() {
  const historyList = $('#history-list');
  if (!historyList) return;
  const history = JSON.parse(localStorage.getItem('offnetpay_history') || '[]');
  
  if (history.length === 0) {
    historyList.innerHTML = '<p style="color:var(--text-3); font-size:14px;">No recent payees yet.</p>';
    $('#clear-history-btn').style.display = 'none';
    return;
  }
  
  $('#clear-history-btn').style.display = 'block';
  historyList.innerHTML = history.map(vpa => `
    <div class="history-item" style="padding:12px 16px; border:1px solid var(--border); margin-bottom:8px; background:var(--surface-hi); cursor:pointer; display:flex; justify-content:space-between; align-items:center;">
      <span style="font-family:var(--mono); font-size:14px; color:var(--text-1);">${vpa}</span>
      <span style="color:var(--lime); font-size:20px;">→</span>
    </div>
  `).join('');
  
  $$('.history-item').forEach(item => {
    item.addEventListener('click', (e) => {
      const vpa = e.currentTarget.querySelector('span').textContent;
      // Switch to pay tab and fill
      $$('.np-tab').forEach(b => b.classList.remove('active'));
      $$('.np-tab[data-tab="pay"]')[0].classList.add('active');
      $('#history-view').style.display = 'none';
      $('#pay-view').style.display = 'block';
      $('#vpa').value = vpa;
      validatePay();
    });
  });
}

if ($('#clear-history-btn')) {
  $('#clear-history-btn').addEventListener('click', () => {
    localStorage.removeItem('offnetpay_history');
    loadHistory();
  });
}

// ─── QR Scanner Logic ───
let html5QrCode;

function startQrScanner() {
  if (!html5QrCode) {
    html5QrCode = new Html5Qrcode("qr-reader");
  }
  
  if (html5QrCode.isScanning) return;

  html5QrCode.start(
    { facingMode: "environment" }, 
    { fps: 10, qrbox: { width: 250, height: 250 } },
    (decodedText, decodedResult) => {
      // On successful scan
      let pa = null;
      if (decodedText.toLowerCase().includes("upi://pay")) {
        const match = decodedText.match(/[?&]pa=([^&]+)/i);
        if (match) pa = decodeURIComponent(match[1]);
      } else if (isValidVPA(decodedText)) {
        pa = decodedText;
      }
      
      if (pa) {
        html5QrCode.stop().then(() => {
          $('#qr-result').style.display = 'block';
          $('#qr-reader').style.display = 'none';
          $('#qr-vpa').textContent = pa;
        }).catch(err => { console.log("Failed to stop scanner", err); });
      }
    },
    (errorMessage) => {
      // Ignore parse errors while scanning
    }
  ).catch(err => {
    console.log("Error starting QR scanner", err);
    $('#qr-reader').innerHTML = `<p style="padding:20px; color:var(--text-3); text-align:center;">Camera access denied or unavailable.</p>`;
  });
}

function stopQrScanner() {
  if (html5QrCode && html5QrCode.isScanning) {
    html5QrCode.stop().catch(err => console.log(err));
  }
}

if ($('#qr-use-btn')) {
  $('#qr-use-btn').addEventListener('click', () => {
    const pa = $('#qr-vpa').textContent;
    $$('.np-tab').forEach(b => b.classList.remove('active'));
    $$('.np-tab[data-tab="pay"]')[0].classList.add('active');
    
    $('#scan-view').style.display = 'none';
    $('#pay-view').style.display = 'block';
    $('#vpa').value = pa;
    validatePay();
    
    $('#qr-result').style.display = 'none';
  });
}

// Init
validatePay();
