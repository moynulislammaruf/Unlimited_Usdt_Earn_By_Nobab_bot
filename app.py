<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Earning Bot</title>
    
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Tiro+Bangla&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --tg-theme-bg-color: var(--tg-bg-color, #1a1a2e);
            --tg-theme-text-color: var(--tg-text-color, #ffffff);
            --tg-theme-button-color: var(--tg-button-color, #7e57c2);
            --tg-theme-button-text-color: var(--tg-button-text-color, #ffffff);
            --tg-theme-hint-color: var(--tg-hint-color, #b0aed4);
            --tg-theme-secondary-bg-color: var(--tg-secondary-bg-color, #242444);
            
            --gradient-start: #4e54c8;
            --gradient-end: #8f94fb;
            --success-color: #00e676;
            --premium-gold: #ffd700;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0; padding: 0;
            background-color: var(--tg-theme-bg-color);
            color: var(--tg-theme-text-color);
            display: flex; flex-direction: column;
            height: 100vh; overflow: hidden;
            -webkit-font-smoothing: antialiased;
        }
        
        #loader {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--tg-theme-bg-color); z-index: 2001;
            display: flex; align-items: center; justify-content: center;
        }
        .spinner {
            border: 4px solid var(--tg-theme-secondary-bg-color);
            border-top: 4px solid var(--tg-theme-button-color);
            border-radius: 50%; width: 40px; height: 40px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .header {
            padding: 20px;
            background: linear-gradient(135deg, #16222A, #3A6073);
            color: white;
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .profile-info { display: flex; align-items: center; gap: 12px; }
        .user-photo { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; border: 2px solid var(--tg-theme-button-color); }
        .user-name { font-weight: 600; font-size: 17px; }
        .user-balance { font-weight: 700; font-size: 22px; color: var(--premium-gold); }
        .user-balance::before { content: '৳'; font-size: 18px; margin-right: 3px; }

        .main-content { flex-grow: 1; padding: 20px; overflow-y: auto; }
        .page-content { display: none; }
        .page-content.active { display: block; animation: fadeIn 0.4s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        
        .stat-card {
            background-color: var(--tg-theme-secondary-bg-color);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 12px; text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .stat-card:hover { transform: translateY(-3px); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .stat-card .icon { color: var(--tg-theme-button-color); margin-bottom: 8px; }
        .stat-card .icon svg { width: 28px; height: 28px; }
        .stat-card h3 { margin: 0 0 5px; font-size: 12px; color: var(--tg-theme-hint-color); font-weight: 500; }
        .stat-card p { margin: 0; font-size: 18px; font-weight: 700; color: var(--tg-theme-text-color); }

        .ad-watch-card {
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            border-radius: 12px; padding: 25px;
            margin-top: 25px; text-align: center;
            color: white;
        }
        #watch-ad-button, #watch-adexora-ad-button {
            width: 100%; padding: 15px; font-size: 18px; font-weight: bold;
            border: none; border-radius: 10px; cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 15px;
        }
        #watch-ad-button {
            background-color: var(--success-color); color: white;
        }
        #watch-adexora-ad-button {
            background-color: #ff8c00; color: white;
        }
        #watch-ad-button:disabled, #watch-adexora-ad-button:disabled { background-color: #555; cursor: not-allowed; }

        .navigation-bar { display: flex; justify-content: space-around; border-top: 1px solid rgba(255, 255, 255, 0.1); padding: 8px 0; background-color: #16222A; position: sticky; bottom: 0; }
        .nav-button { background: none; border: none; cursor: pointer; color: var(--tg-theme-hint-color); display: flex; flex-direction: column; align-items: center; gap: 4px; flex-grow: 1; padding: 5px 0; }
        .nav-button svg { width: 24px; height: 24px; stroke-width: 2; }
        .nav-button span { font-size: 12px; font-weight: 500; }
        .nav-button.active { color: var(--tg-theme-button-color); }
        
        .card { background-color: var(--tg-theme-secondary-bg-color); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
        h1 { font-size: 24px; margin-bottom: 20px; font-weight: 700; }
        .task-list { list-style: none; padding: 0; }
        .task-item { display: flex; align-items: center; gap: 15px; padding: 15px; background-color: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.1); cursor: pointer; transition: background-color 0.2s; }
        .task-item:hover { background-color: rgba(153, 153, 153, 0.2); }
        .task-item[disabled] { cursor: not-allowed; opacity: 0.6; }
        .task-item-details { flex-grow: 1; }
        .task-item .icon-container { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background-color: rgba(0,0,0,0.2); }
        .task-item .icon-container svg { width: 24px; height: 24px; }
        .task-reward { font-size: 16px; font-weight: bold; color: var(--success-color); }
        .task-completed { color: var(--tg-theme-hint-color); font-weight: bold; }
        
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 500; color: var(--tg-theme-hint-color); }
        input, select { width: 100%; padding: 14px; box-sizing: border-box; background-color: var(--tg-theme-bg-color); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; color: var(--tg-theme-text-color); font-size: 16px; }
        
        .refer-hero { text-align: center; margin-bottom: 25px; }
        .refer-hero h1 { font-size: 24px; font-weight: 700; color: var(--tg-theme-text-color); margin-bottom: 5px; }
        .refer-hero p { font-size: 15px; color: var(--tg-theme-hint-color); max-width: 300px; margin: 0 auto; }
        .referral-link-card { background-color: var(--tg-theme-secondary-bg-color); border-radius: 12px; padding: 10px; display: flex; align-items: center; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
        #referral-link { flex-grow: 1; background: none; border: none; color: var(--tg-theme-text-color); font-size: 14px; padding: 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        #copy-button { padding: 10px 15px; border: none; background-color: var(--tg-theme-button-color); color: var(--tg-theme-button-text-color); border-radius: 8px; cursor: pointer; font-weight: 600; }
        
        .action-button {
            display: block; width: 100%; text-align: center;
            color: white; padding: 15px; border-radius: 10px;
            font-size: 16px; font-weight: 600; text-decoration: none; border: none; cursor: pointer;
            box-sizing: border-box;
        }
        .action-button.primary { background-color: var(--tg-theme-button-color); }
        .action-button.success { background-color: var(--success-color); }
        .action-button:disabled { background-color: #555; color: #999; cursor: not-allowed; }

        .modal-overlay {
            display: none; position: fixed; z-index: 2000;
            left: 0; top: 0; width: 100%; height: 100%;
            overflow: auto; background-color: rgba(0,0,0,0.6);
            animation: fadeInModal 0.3s;
        }
        .modal-content {
            background-color: var(--tg-theme-secondary-bg-color);
            margin: 40% auto; padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px; width: 85%; max-width: 400px;
            position: relative; box-shadow: 0 5px 25px rgba(0,0,0,0.3);
        }
        .modal-close-btn {
            color: #aaa; position: absolute; top: 10px; right: 15px;
            font-size: 28px; font-weight: bold; cursor: pointer;
        }
        .modal-close-btn:hover { color: white; }
        #notice-text {
            font-family: 'Tiro Bangla', serif;
            font-size: 18px; line-height: 1.6;
            color: var(--tg-theme-text-color);
            white-space: pre-wrap;
        }
        @keyframes fadeInModal { from { opacity: 0; } to { opacity: 1; } }
    </style>
<link rel="me" href="https://draft.blogger.com/profile/08399734943958828825" />
<meta name='google-adsense-platform-account' content='ca-host-pub-1556223355139109'/>
<meta name='google-adsense-platform-domain' content='blogspot.com'/>
</head>
<body>
    <div id="loader"><div class="spinner"></div></div>

    <div id="notice-modal" class="modal-overlay">
        <div class="modal-content">
            <span id="close-notice-modal" class="modal-close-btn">&times;</span>
            <h2 style="margin-top:0; color: var(--tg-theme-button-color);">নোটিশ</h2>
            <p id="notice-text"></p>
        </div>
    </div>
    
    <header class="header">
        <div class="profile-info">
            <img id="user-photo" class="user-photo" alt="P" src="">
            <div>
                <span id="user-name" class="user-name">Loading...</span>
            </div>
        </div>
        <div class="balance-info">
            <span id="user-balance" class="user-balance">0.00</span>
        </div>
    </header>
    
    <main class="main-content">
        <div id="home" class="page-content active">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg></div>
                    <h3>দৈনিক বিজ্ঞাপন</h3>
                    <p><span id="ads-watched-today">0</span> / <span id="ads-daily-limit">...</span></p>
                </div>
                 <div class="stat-card">
                    <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><line x1="23" y1="11" x2="17" y2="11"></line></svg></div>
                    <h3>মোট রেফার</h3>
                    <p id="total-referrals">0</p>
                </div>
                <div class="stat-card">
                    <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg></div>
                    <h3>মোট উপার্জন</h3>
                    <p>৳<span id="total-earned">0.00</span></p>
                </div>
                <div class="stat-card">
                    <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg></div>
                    <h3>মোট উত্তোলন</h3>
                    <p>৳<span id="total-withdrawn">0.00</span></p>
                </div>
            </div>
             
            <div class="ad-watch-card">
                <h2>দৈনিক আয় করুন</h2>
                <p>ভিডিও বিজ্ঞাপন দেখে প্রতিদিন আয় করার সুযোগ!</p>
                <button id="watch-ad-button" class="action-button success">বিজ্ঞাপন দেখুন #1 (Monetag)</button>
                <button id="watch-adexora-ad-button" class="action-button">বিজ্ঞাপন দেখুন #2 (Adexora)</button>
            </div>
        </div>

        <div id="task" class="page-content">
            <div id="task-list-view">
                <h1>উপলব্ধ কাজ</h1>
                <p>কাজটি সম্পন্ন করতে টাস্কের ওপর ক্লিক করুন। কাজটি শুরু করার পর ৩০ সেকেন্ড অপেক্ষা করে পুরস্কার সংগ্রহ করতে হবে।</p>
                <ul id="task-list" class="task-list"></ul>
            </div>
            <div id="task-in-progress-view" style="display: none;">
                <div class="card">
                    <h2 id="inprogress-title" style="margin-top: 0;"></h2>
                    <p id="inprogress-desc"></p>
                    <button id="inprogress-link-btn" class="action-button primary">কাজ শুরু করুন</button>
                    <button id="inprogress-claim-btn" class="action-button success" style="margin-top: 15px;" disabled>পুরস্কার সংগ্রহ করুন</button>
                </div>
                <button id="inprogress-back-btn" style="background: none; border: 1px solid var(--tg-theme-hint-color); color: var(--tg-theme-hint-color);" class="action-button">ফিরে যান</button>
            </div>
        </div>

        <div id="refer" class="page-content">
             <div class="refer-hero">
                <h1>বন্ধুদের আমন্ত্রণ জানান</h1>
                <p>আপনার রেফারেল লিঙ্ক শেয়ার করুন এবং আমাদের কমিউনিটি বাড়াতে সাহায্য করুন।</p>
             </div>
             <div class="referral-link-card">
                <input type="text" id="referral-link" readonly value="লিঙ্ক তৈরি হচ্ছে...">
                <button id="copy-button">লিঙ্ক কপি করুন</button>
             </div>
             
             <div class="stats-grid" style="margin-bottom: 20px;">
                <div class="stat-card" style="padding: 20px;">
                    <h3>প্রতি রেফারে বোনাস</h3>
                    <p>৳<span id="referral-bonus-display">0.00</span></p>
                </div>
                <div class="stat-card" style="padding: 20px;">
                    <h3>রেফার কমিশন</h3>
                    <p><span id="referral-commission-display">0</span>%</p>
                </div>
             </div>

             <div class="stat-card" style="background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)); color: white; padding: 25px;">
                <h3 style="color: white; opacity: 0.8; font-size: 16px;">আপনার মোট রেফারেল</h3>
                <p id="total-referrals-display" style="font-size: 36px; color: white;">0</p>
             </div>
        </div>
        
        <div id="withdraw" class="page-content">
            <h1>ব্যালেন্স উত্তোলন</h1>
            <p id="min-withdraw-text">অনুগ্রহ করে একটি পেমেন্ট মাধ্যম নির্বাচন করুন।</p>
            <div class="card">
                <div class="form-group">
                    <label for="withdraw-method">পেমেন্ট মাধ্যম</label>
                    <select id="withdraw-method"></select>
                </div>
                <div class="form-group">
                    <label for="account-number">অ্যাকাউন্ট নম্বর</label>
                    <input type="text" id="account-number" placeholder="আপনার অ্যাকাউন্ট নম্বর দিন">
                </div>
                <div class="form-group">
                    <label for="amount">টাকার পরিমাণ</label>
                    <input type="number" id="amount" placeholder="টাকার পরিমাণ লিখুন">
                </div>
                <button id="withdraw-button" class="action-button success">উত্তোলন করুন</button>
            </div>
        </div>

        <div id="support" class="page-content">
            <h1>সাপোর্ট ও সহায়তা</h1><p>কোনো সমস্যা বা প্রশ্ন থাকলে আমাদের সাথে যোগাযোগ করুন।</p>
            <div class="card">
                 <h2>যোগাযোগ করুন</h2><p>আপনার যেকোনো সমস্যায় বা প্রশ্নের জন্য আমাদের সাপোর্ট টিমের সাথে সরাসরি যোগাযোগ করতে পারেন।</p>
                 <a href="#" id="support-channel-link" target="_blank" class="action-button primary" style="margin-bottom:15px;">টেলিগ্রাম চ্যানেলে যোগ দিন</a>
                 <a href="#" id="support-chat-link" target="_blank" class="action-button" style="background:none; border: 1px solid var(--tg-theme-button-color); color: var(--tg-theme-button-color);">সাপোর্টের জন্য মেসেজ করুন</a>
            </div>
        </div>
    </main>
    
    <nav id="navigation-bar" class="navigation-bar">
        <button class="nav-button active" data-target="home"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg><span>হোম</span></button>
        <button class="nav-button" data-target="task"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg><span>টাস্ক</span></button>
        <button class="nav-button" data-target="refer"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg><span>রেফার</span></button>
        <button class="nav-button" data-target="withdraw"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg><span>উত্তোলন</span></button>
        <button class="nav-button" data-target="support"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg><span>সাপোর্ট</span></button>
    </nav>

    <div id="monetag-ad-container"></div>

    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-database-compat.js"></script>
    
    <script>
    document.addEventListener('DOMContentLoaded', () => {
        const firebaseConfig = {
  apiKey: "AIzaSyAMflUr-eRgBqUcBMINOPz935cXPNnZhok",
  authDomain: "royal-b07ae.firebaseapp.com",
  databaseURL: "https://royal-b07ae-default-rtdb.firebaseio.com",
  projectId: "royal-b07ae",
  storageBucket: "royal-b07ae.firebasestorage.app",
  messagingSenderId: "466563188024",
  appId: "1:466563188024:web:1e53b917f3b45a66e92dcd"
};
        firebase.initializeApp(firebaseConfig);
        const database = firebase.database();
        
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
        tg.setHeaderColor('#16222A');

        let siteConfig = {};
        let currentUser = {};
        const tgUser = tg.initDataUnsafe.user || { id: `test_user_${Date.now()}`, first_name: 'Test', last_name: 'User', photo_url: null };
        const userRef = database.ref('users/' + tgUser.id);
        
        let taskTimerInterval = null;
        const noticeModal = document.getElementById('notice-modal');

        function initializeApp() {
            database.ref('config').on('value', snapshot => {
                siteConfig = snapshot.val() || {};
                
                if (siteConfig.notice && siteConfig.notice.trim() !== '') {
                    document.getElementById('notice-text').innerText = siteConfig.notice;
                    noticeModal.style.display = 'block';
                }

                updateConfigUI();
                updateAdButtonsState();
                loadMonetagScript();
                loadAdexoraScript();
            });

            userRef.on('value', snapshot => {
                const isNewUser = !snapshot.exists();
                const fullName = `${tgUser.first_name || ''} ${tgUser.last_name || ''}`.trim() || 'Guest';
                
                currentUser = isNewUser ? {
                    balance: 0, totalEarned: 0, totalWithdrawn: 0, 
                    adsWatchedMonetag: 0, adsWatchedAdexora: 0,
                    totalReferrals: 0, 
                    fullName: fullName, completedTasks: {}, 
                    createdAt: new Date().toISOString()
                } : snapshot.val();
                
                if (isNewUser) {
                    const referrerId = tg.initDataUnsafe.start_param;
                    if (referrerId && referrerId !== tgUser.id.toString()) {
                        currentUser.referredBy = referrerId;
                        handleReferral(referrerId);
                    }
                    userRef.set(currentUser);
                }

                document.getElementById('user-name').textContent = fullName;
                document.getElementById('user-photo').src = tgUser.photo_url || 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI2NjYyI+PHBhdGggZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6bTAgM2MxLjY2IDAgMyAxLjM0IDMgMyAwIDEuNjYtMS4zNCAzLTMgMy0xLjY2IDAtMy0xLjM0LTMtMyAwLTEuNjYgMS4zNC0zIDMtM3ptMCAxNGMtMi4wMyAwLTMuNDQtMC44OC00LjAwLTEuNzEuNDYtMC44MyAxLjkxLTEuNDYgNC0xLjQ2czMuNTQgMC42MyA0IDEuNDZjLTAuNTYgMC44My0xLjk3IDEuNzEtNCAxLjcxeiIvPjwvc3ZnPg==';

                updateUserUI();
                updateAdButtonsState();
                loadTasks();
            });

            document.getElementById('loader').style.display = 'none';
        }
        
        function handleReferral(referrerId) {
            const referrerRef = database.ref(`users/${referrerId}`);
            referrerRef.transaction(referrerData => {
                if (referrerData) {
                    const bonusAmount = parseFloat(siteConfig.referralBonus || 0);
                    referrerData.totalReferrals = (referrerData.totalReferrals || 0) + 1;
                    if (bonusAmount > 0) {
                        referrerData.balance = (referrerData.balance || 0) + bonusAmount;
                        referrerData.totalEarned = (referrerData.totalEarned || 0) + bonusAmount;
                    }
                }
                return referrerData;
            });
        }

        function applyReferralCommission(earnedAmount) {
            if (!currentUser.referredBy || !siteConfig.referralCommissionPercentage || siteConfig.referralCommissionPercentage <= 0) return;
            const referrerRef = database.ref(`users/${currentUser.referredBy}`);
            const commissionRate = parseFloat(siteConfig.referralCommissionPercentage);
            const commissionAmount = (earnedAmount * commissionRate) / 100;
            if (commissionAmount <= 0) return;
            referrerRef.transaction(referrerData => {
                if (referrerData) {
                    referrerData.balance = (referrerData.balance || 0) + commissionAmount;
                    referrerData.totalEarned = (referrerData.totalEarned || 0) + commissionAmount;
                }
                return referrerData;
            });
        }

        function loadMonetagScript() {
            const container = document.getElementById('monetag-ad-container');
            const zoneId = siteConfig.monetagZoneId;
            if (!zoneId || document.querySelector(`script[data-zone='${zoneId}']`)) return;
            container.innerHTML = '';
            const script = document.createElement('script');
            script.src = '//libtl.com/sdk.js';
            script.dataset.zone = zoneId;
            script.dataset.sdk = `show_${zoneId}`;
            script.onerror = () => console.error("Failed to load Monetag script.");
            container.appendChild(script);
        }

        function loadAdexoraScript() {
            const zoneId = siteConfig.adexoraZoneId;
            if (!zoneId || document.querySelector(`script[src*='adexora.com'][src*='id=${zoneId}']`)) return;
            const script = document.createElement('script');
            script.src = `https://adexora.com/cdn/ads.js?id=${zoneId}`;
            script.onerror = () => console.error("Failed to load Adexora script.");
            document.body.appendChild(script);
        }
        
        function updateUserUI() {
            const totalAdsWatched = (currentUser.adsWatchedMonetag || 0) + (currentUser.adsWatchedAdexora || 0);
            document.getElementById('ads-watched-today').textContent = totalAdsWatched;
            document.getElementById('user-balance').textContent = (currentUser.balance || 0).toFixed(2);
            document.getElementById('total-referrals').textContent = currentUser.totalReferrals || 0;
            document.getElementById('total-earned').textContent = (currentUser.totalEarned || 0).toFixed(2);
            document.getElementById('total-withdrawn').textContent = (currentUser.totalWithdrawn || 0).toFixed(2);
            document.getElementById('total-referrals-display').textContent = currentUser.totalReferrals || 0;
        }

        function updateConfigUI() {
            const totalAdLimit = (siteConfig.monetagDailyAdLimit || 0) + (siteConfig.adexoraDailyAdLimit || 0);
            document.getElementById('ads-daily-limit').textContent = totalAdLimit;
            document.getElementById('referral-bonus-display').textContent = (siteConfig.referralBonus || 0).toFixed(2);
            document.getElementById('referral-commission-display').textContent = siteConfig.referralCommissionPercentage || 0;
            document.getElementById('support-channel-link').href = siteConfig.supportLinks?.channel || '#';
            document.getElementById('support-chat-link').href = siteConfig.supportLinks?.chat || '#';
            
            // --- এই অংশটি আপনার দেওয়া ফাইল অনুযায়ী পরিবর্তন করা হয়েছে ---
            const miniAppUrl = `t.me/ROYALEARN_BD_BOT/app`;
            document.getElementById('referral-link').value = `${miniAppUrl}?startapp=${tgUser.id}`;
            // --- পরিবর্তন শেষ ---

            const withdrawMethodSelect = document.getElementById('withdraw-method');
            withdrawMethodSelect.innerHTML = '<option value="" disabled selected>একটি মাধ্যম নির্বাচন করুন</option>';
            if (siteConfig.paymentMethods) {
                Object.keys(siteConfig.paymentMethods).forEach(key => {
                    const method = siteConfig.paymentMethods[key];
                    if(method && method.name) {
                        const option = new Option(method.name, key);
                        option.dataset.min = method.minWithdrawal || 0;
                        withdrawMethodSelect.appendChild(option);
                    }
                });
            }
        }

        function updateAdButtonsState() {
            if (!currentUser || !siteConfig) return;
            const adButton = document.getElementById('watch-ad-button');
            const adexoraButton = document.getElementById('watch-adexora-ad-button');
            const monetagLimitReached = (currentUser.adsWatchedMonetag || 0) >= (siteConfig.monetagDailyAdLimit || 0);
            adButton.disabled = monetagLimitReached;
            if(monetagLimitReached) adButton.textContent = "আজকের সীমা শেষ #1"; else adButton.textContent = "বিজ্ঞাপন দেখুন #1 (Monetag)";
            
            const adexoraLimitReached = (currentUser.adsWatchedAdexora || 0) >= (siteConfig.adexoraDailyAdLimit || 0);
            adexoraButton.disabled = adexoraLimitReached;
            if(adexoraLimitReached) adexoraButton.textContent = "আজকের সীমা শেষ #2"; else adexoraButton.textContent = "বিজ্ঞাপন দেখুন #2 (Adexora)";
        }
        
        function processAdReward(adType) {
            const adReward = adType === 'Monetag' ? parseFloat(siteConfig.monetagAdReward || 0) : parseFloat(siteConfig.adexoraAdReward || 0);
            if (adReward <= 0) return;
            const updates = {};
            const adCounterKey = adType === 'Monetag' ? 'adsWatchedMonetag' : 'adsWatchedAdexora';
            updates[`/users/${tgUser.id}/balance`] = firebase.database.ServerValue.increment(adReward);
            updates[`/users/${tgUser.id}/totalEarned`] = firebase.database.ServerValue.increment(adReward);
            updates[`/users/${tgUser.id}/${adCounterKey}`] = firebase.database.ServerValue.increment(1);
            database.ref().update(updates).then(() => {
                tg.HapticFeedback.notificationOccurred('success');
                applyReferralCommission(adReward);
            }).catch(error => tg.showAlert('একটি ত্রুটি ঘটেছে: ' + error.message));
        }

        function getCategoryIcon(category) {
            const icons = {
                youtube: `<svg fill="#ff0000" viewBox="0 0 24 24"><path d="M21.582,6.186c-0.23-0.86-0.908-1.538-1.768-1.768C18.267,4,12,4,12,4S5.733,4,4.186,4.418 c-0.86,0.23-1.538,0.908-1.768,1.768C2,7.733,2,12,2,12s0,4.267,0.418,5.814c0.23,0.86,0.908,1.538,1.768,1.768 C5.733,20,12,20,12,20s6.267,0,7.814-0.418c0.861-0.23,1.538-0.908,1.768-1.768C22,16.267,22,12,22,12S22,7.733,21.582,6.186z M10,15.464V8.536L16,12L10,15.464z"/></svg>`,
                telegram: `<svg fill="#2AABEE" viewBox="0 0 24 24"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.58c-.28 1.13-1.04 1.4-1.74 .88l-4.98-3.6-2.32 2.2a1.06 1.06 0 0 1-.9.27z"/></svg>`,
                facebook: `<svg fill="#1877F2" viewBox="0 0 24 24"><path d="M12 2.04C6.5 2.04 2 6.53 2 12.06c0 5.52 4.5 10.02 10 10.02c5.5 0 10-4.5 10-10.02C22 6.53 17.5 2.04 12 2.04zM16.5 12.62h-2.1v6.94h-3.2v-6.94H9.5v-2.8h1.7V8.04c0-1.7.9-2.7 2.7-2.7h2.1v2.8h-1.4c-.6 0-.7.3-.7.7v1.4h2.1l-.3 2.8z"/></svg>`
            };
            return `<div class="icon-container">${icons[category] || ''}</div>`;
        }
        function loadTasks() {
            const taskList = document.getElementById('task-list');
            database.ref('tasks').on('value', snapshot => {
                taskList.innerHTML = '';
                if (!snapshot.exists()) { taskList.innerHTML = '<p style="text-align:center; color: var(--tg-theme-hint-color);">এই মুহূর্তে কোনো কাজ উপলব্ধ নেই।</p>'; return; }
                snapshot.forEach(child => {
                    const taskId = child.key, task = child.val();
                    const isCompleted = currentUser.completedTasks && currentUser.completedTasks[taskId];
                    const li = document.createElement('li');
                    li.className = 'task-item';
                    li.innerHTML = `${getCategoryIcon(task.category)}<div class="task-item-details"><h3 style="margin:0;">${task.title}</h3><p style="margin:5px 0 0;font-size:13px;color:var(--tg-theme-hint-color);">${task.description}</p></div><span class="task-reward">${isCompleted ? '<span class="task-completed">সম্পন্ন</span>' : `+ ৳${task.reward}`}</span>`;
                    if (isCompleted) { li.setAttribute('disabled', 'true'); } else { li.addEventListener('click', () => handleTask(taskId, task)); }
                    taskList.appendChild(li);
                });
            });
        }
        function handleTask(taskId, task) {
            document.getElementById('task-list-view').style.display = 'none';
            document.getElementById('task-in-progress-view').style.display = 'block';
            document.getElementById('inprogress-title').textContent = task.title;
            document.getElementById('inprogress-desc').textContent = task.description;
            const linkBtn = document.getElementById('inprogress-link-btn'), claimBtn = document.getElementById('inprogress-claim-btn');
            linkBtn.onclick = () => {
                tg.openLink(task.url);
                linkBtn.disabled = true;
                let countdown = 30;
                claimBtn.textContent = `পুরস্কার সংগ্রহ করুন (${countdown}s)`;
                taskTimerInterval = setInterval(() => {
                    countdown--;
                    claimBtn.textContent = `পুরস্কার সংগ্রহ করুন (${countdown}s)`;
                    if (countdown <= 0) { clearInterval(taskTimerInterval); claimBtn.disabled = false; claimBtn.textContent = 'পুরস্কার সংগ্রহ করুন'; }
                }, 1000);
            };
            claimBtn.onclick = () => {
                const reward = parseFloat(task.reward);
                const updates = {};
                updates[`/users/${tgUser.id}/balance`] = firebase.database.ServerValue.increment(reward);
                updates[`/users/${tgUser.id}/totalEarned`] = firebase.database.ServerValue.increment(reward);
                updates[`/users/${tgUser.id}/completedTasks/${taskId}`] = true;
                database.ref().update(updates).then(() => {
                    tg.HapticFeedback.notificationOccurred('success');
                    tg.showAlert(`অভিনন্দন! আপনি ৳${reward.toFixed(2)} আয় করেছেন।`);
                    applyReferralCommission(reward);
                    showMainTaskView();
                });
            };
        }
        function showMainTaskView() {
            clearInterval(taskTimerInterval);
            document.getElementById('task-list-view').style.display = 'block';
            document.getElementById('task-in-progress-view').style.display = 'none';
            document.getElementById('inprogress-link-btn').disabled = false;
            document.getElementById('inprogress-claim-btn').disabled = true;
            document.getElementById('inprogress-claim-btn').textContent = 'পুরস্কার সংগ্রহ করুন';
        }
        document.getElementById('inprogress-back-btn').addEventListener('click', showMainTaskView);

        document.getElementById('watch-ad-button').addEventListener('click', function() {
            const adButton = this, zoneId = siteConfig.monetagZoneId;
            if (!zoneId) return tg.showAlert("এই মুহূর্তে কোনো বিজ্ঞাপন উপলব্ধ নেই।");
            try {
                if (typeof window[`show_${zoneId}`] === 'function') {
                    window[`show_${zoneId}`]();
                } else {
                    tg.showAlert('বিজ্ঞাপন লোড হতে সমস্যা হচ্ছে।'); return;
                }
            } catch (e) { console.error('Monetag Ad error:', e); tg.showAlert('বিজ্ঞাপন দেখাতে ব্যর্থ হয়েছে।'); return; }
            
            adButton.disabled = true;
            const timerDuration = parseInt(siteConfig.monetagAdTimer || 15);
            let countdown = timerDuration;
            adButton.textContent = `অপেক্ষা করুন... ${countdown}s`;
            
            const timer = setInterval(() => {
                countdown--;
                if(countdown >= 0) adButton.textContent = `অপেক্ষা করুন... ${countdown}s`;
                else clearInterval(timer);
            }, 1000);
            
            setTimeout(() => {
                processAdReward('Monetag');
                tg.showAlert(`অভিনন্দন! আপনি ৳${(siteConfig.monetagAdReward || 0).toFixed(2)} আয় করেছেন।`);
            }, timerDuration * 1000);
        });
        
        document.getElementById('watch-adexora-ad-button').addEventListener('click', function() {
            const adexoraButton = this;
            if (!siteConfig.adexoraZoneId) return tg.showAlert("এই মুহূর্তে কোনো Adexora বিজ্ঞাপন উপলব্ধ নেই।");
            if (typeof window.showAdexora !== 'function') return tg.showAlert("Adexora বিজ্ঞাপন এখনো লোড হয়নি, অনুগ্রহ করে কয়েক সেকেন্ড পর আবার চেষ্টা করুন।");

            adexoraButton.disabled = true;
            adexoraButton.textContent = "বিজ্ঞাপন লোড হচ্ছে...";

            window.showAdexora()
                .then(() => {
                    console.log("Adexora ad completed successfully.");
                    tg.showAlert(`বিজ্ঞাপন দেখা সফল হয়েছে! আপনি ৳${(siteConfig.adexoraAdReward || 0).toFixed(2)} আয় করেছেন।`);
                    processAdReward('Adexora');
                })
                .catch(error => {
                    console.error("Adexora ad failed:", error);
                    tg.showAlert("বিজ্ঞাপন দেখানো সম্ভব হয়নি। কোনো বিজ্ঞাপন উপলব্ধ নাও থাকতে পারে অথবা আপনি এটি আগেভাগেই বন্ধ করে দিয়েছেন।");
                })
                .finally(() => {
                    // This will run whether the ad was successful or not,
                    // resetting the button after a short delay.
                    // The on('value') listener will handle the correct button state (enabled/disabled).
                    setTimeout(updateAdButtonsState, 500); 
                });
        });

        document.getElementById('navigation-bar').addEventListener('click', e => {
            const navButton = e.target.closest('.nav-button');
            if (!navButton) return;
            document.querySelector('.nav-button.active')?.classList.remove('active');
            document.querySelector('.page-content.active')?.classList.remove('active');
            navButton.classList.add('active');
            document.getElementById(navButton.dataset.target).classList.add('active');
            if(navButton.dataset.target === 'task') showMainTaskView();
        });
        document.getElementById('copy-button').addEventListener('click', () => {
            navigator.clipboard.writeText(document.getElementById('referral-link').value).then(() => {
                tg.HapticFeedback.notificationOccurred('success');
                tg.showAlert('রেফারেল লিঙ্ক কপি করা হয়েছে!');
            });
        });
        document.getElementById('withdraw-method').addEventListener('change', (e) => {
            const selectedOption = e.target.options[e.target.selectedIndex];
            const minAmount = selectedOption.dataset.min;
            document.getElementById('min-withdraw-text').textContent = minAmount ? `এই মাধ্যমে ন্যূনতম উত্তোলন সীমা ৳${minAmount}।` : 'একটি পেমেন্ট মাধ্যম নির্বাচন করুন।';
        });
        document.getElementById('withdraw-button').addEventListener('click', () => {
            const methodSelect = document.getElementById('withdraw-method'), selectedOption = methodSelect.options[methodSelect.selectedIndex], methodKey = selectedOption.value;
            if (!methodKey) return tg.showAlert('অনুগ্রহ করে একটি পেমেন্ট মাধ্যম নির্বাচন করুন।');
            const amount = parseFloat(document.getElementById('amount').value), account = document.getElementById('account-number').value.trim();
            const minWithdrawal = parseFloat(selectedOption.dataset.min || 0), minReferrals = parseInt(siteConfig.minReferralsForWithdrawal || 0);
            if ((currentUser.totalReferrals || 0) < minReferrals) return tg.showAlert(`উত্তোলন করার জন্য আপনার ন্যূনতম ${minReferrals} জন রেফারেলের প্রয়োজন।`);
            if (!account || !amount) return tg.showAlert('অনুগ্রহ করে সব তথ্য পূরণ করুন।');
            if (isNaN(amount) || amount <= 0) return tg.showAlert('টাকার পরিমাণ সঠিক নয়।');
            if (amount < minWithdrawal) return tg.showAlert(`ন্যূনতম উত্তোলন সীমা ৳${minWithdrawal}।`);
            if (amount > currentUser.balance) return tg.showAlert('আপনার অ্যাকাউন্টে পর্যাপ্ত ব্যালেন্স নেই।');
            
            document.getElementById('withdraw-button').disabled = true;
            userRef.child('balance').set(firebase.database.ServerValue.increment(-amount))
                .then(() => {
                    const request = { userId: tgUser.id, userName: currentUser.fullName, method: siteConfig.paymentMethods[methodKey].name, account, amount, status: 'pending', timestamp: new Date().toISOString() };
                    database.ref('withdrawal_requests').push(request).then(() => {
                        tg.HapticFeedback.notificationOccurred('success');
                        tg.showAlert('আপনার উত্তোলনের অনুরোধটি সফলভাবে জমা হয়েছে।');
                        document.getElementById('amount').value = '';
                        document.getElementById('account-number').value = '';
                    }).catch(error => {
                        tg.showAlert("অনুরোধ জমা দিতে সমস্যা হয়েছে: " + error.message);
                        userRef.child('balance').set(firebase.database.ServerValue.increment(amount)); // Revert balance
                    });
                })
                .catch(err => {
                    tg.showAlert("ব্যালেন্স আপডেট করা যায়নি: " + err.message);
                })
                .finally(() => {
                    document.getElementById('withdraw-button').disabled = false;
                });
        });
        
        document.getElementById('close-notice-modal').onclick = () => noticeModal.style.display = "none";
        window.onclick = (event) => { if (event.target == noticeModal) { noticeModal.style.display = "none"; } };
        
        initializeApp();
    });
    </script>
</body>
</html>
