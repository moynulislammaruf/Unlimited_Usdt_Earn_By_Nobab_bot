
export interface UserData {
  id: string;
  name: string;
  balance: number;
  referCount: number;
  referredBy?: string;
  dailyAds: number;
  dailyTempleRun: number;
  dailyColorGame: number;
  dailySpin: number;
  dailyTap: number;
  lastDate: string;
}

export interface WithdrawalRequest {
  id: string;
  uid: string;
  amount: number;
  method: string;
  number: string;
  status: 'pending' | 'approved' | 'rejected';
  timestamp: any;
}

export interface Task {
  name: string;
  link: string;
}

export interface AppConfig {
  websitesToVisit: Task[];
  socialTasks: Task[];
}

export enum Page {
  Overview = 'overview',
  Users = 'users',
  Withdrawals = 'withdrawals',
  Tasks = 'tasks'
}
