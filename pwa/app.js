const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

// ─── Tab Switching ───
$$('.np-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('.np-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const isBalance = btn.dataset.tab === 'balance';
    $('#pay-view').style.display    = isBalance ? 'none' : 'block';
    $('#bal-view').style.display    = isBalance ? 'block' : 'none';
    $('#result-view').style.display = 'none';
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

// Init
validatePay();
