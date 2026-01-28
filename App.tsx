
import React, { useState, useEffect } from 'react';
import { LayoutDashboard, Users, CreditCard, ListChecks, Search, LogOut } from 'lucide-react';
import { Page } from './types';
import Overview from './components/Overview';
import UserManagement from './components/UserManagement';
import WithdrawalManagement from './components/WithdrawalManagement';
import TaskManagement from './components/TaskManagement';

const App: React.FC = () => {
  const [activePage, setActivePage] = useState<Page>(Page.Overview);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessKey, setAccessKey] = useState('');

  const handleLogin = () => {
    // Simple access control for admin demonstration
    if (accessKey === 'admin123') {
      setIsAuthenticated(true);
    } else {
      alert('Invalid Admin Key');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#050505] p-4">
        <div className="ultra-card p-8 w-full max-w-md text-center">
          <h1 className="orbitron text-2xl text-yellow-500 mb-6">ADMIN ACCESS</h1>
          <input 
            type="password" 
            placeholder="Enter Admin Secret"
            className="w-full bg-black border border-white/10 rounded-lg p-3 mb-4 outline-none focus:border-yellow-500 transition-colors"
            value={accessKey}
            onChange={(e) => setAccessKey(e.target.value)}
          />
          <button 
            onClick={handleLogin}
            className="btn-pro w-full py-3"
          >
            ENTER DASHBOARD
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-[#050505]">
      {/* Sidebar */}
      <aside className="w-64 bg-black border-r border-white/5 flex flex-col hidden md:flex">
        <div className="p-6 border-b border-white/5">
          <h1 className="orbitron text-yellow-500 font-bold text-lg">CASHREWARD PRO</h1>
          <p className="text-[10px] text-gray-500 tracking-widest uppercase">Admin Terminal</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          <NavItem 
            icon={<LayoutDashboard size={20} />} 
            label="Overview" 
            active={activePage === Page.Overview}
            onClick={() => setActivePage(Page.Overview)}
          />
          <NavItem 
            icon={<Users size={20} />} 
            label="Users" 
            active={activePage === Page.Users}
            onClick={() => setActivePage(Page.Users)}
          />
          <NavItem 
            icon={<CreditCard size={20} />} 
            label="Withdrawals" 
            active={activePage === Page.Withdrawals}
            onClick={() => setActivePage(Page.Withdrawals)}
          />
          <NavItem 
            icon={<ListChecks size={20} />} 
            label="Tasks Config" 
            active={activePage === Page.Tasks}
            onClick={() => setActivePage(Page.Tasks)}
          />
        </nav>

        <div className="p-4 border-t border-white/5">
          <button 
            onClick={() => setIsAuthenticated(false)}
            className="flex items-center gap-3 text-red-500 hover:bg-red-500/10 w-full p-3 rounded-lg transition-colors"
          >
            <LogOut size={20} />
            <span className="font-semibold">Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="h-16 border-b border-white/5 bg-[#050505]/50 backdrop-blur-md sticky top-0 z-30 flex items-center justify-between px-8">
          <h2 className="orbitron text-lg capitalize">{activePage.replace('-', ' ')}</h2>
          <div className="flex items-center gap-4">
             <div className="text-right">
                <p className="text-xs font-bold">Admin Master</p>
                <div className="text-[8px] text-green-500 uppercase font-bold tracking-widest">System Online</div>
             </div>
             <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-yellow-500 to-red-600 border border-white/10" />
          </div>
        </header>

        <div className="p-8">
          {activePage === Page.Overview && <Overview />}
          {activePage === Page.Users && <UserManagement />}
          {activePage === Page.Withdrawals && <WithdrawalManagement />}
          {activePage === Page.Tasks && <TaskManagement />}
        </div>
      </main>

      {/* Mobile Nav */}
      <nav className="md:hidden fixed bottom-0 w-full bg-black/90 backdrop-blur-xl border-t border-white/5 p-4 flex justify-around z-50">
        <button onClick={() => setActivePage(Page.Overview)} className={activePage === Page.Overview ? 'text-yellow-500' : 'text-gray-500'}><LayoutDashboard /></button>
        <button onClick={() => setActivePage(Page.Users)} className={activePage === Page.Users ? 'text-yellow-500' : 'text-gray-500'}><Users /></button>
        <button onClick={() => setActivePage(Page.Withdrawals)} className={activePage === Page.Withdrawals ? 'text-yellow-500' : 'text-gray-500'}><CreditCard /></button>
        <button onClick={() => setActivePage(Page.Tasks)} className={activePage === Page.Tasks ? 'text-yellow-500' : 'text-gray-500'}><ListChecks /></button>
      </nav>
    </div>
  );
};

interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  active: boolean;
  onClick: () => void;
}

const NavItem: React.FC<NavItemProps> = ({ icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all ${
      active 
        ? 'bg-gradient-to-r from-yellow-500/20 to-red-500/20 border border-yellow-500/30 text-yellow-500' 
        : 'text-gray-400 hover:bg-white/5 hover:text-white'
    }`}
  >
    {icon}
    <span className="font-semibold text-sm">{label}</span>
  </button>
);

export default App;
