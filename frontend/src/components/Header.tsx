"use client";

import { Search, Bell } from "lucide-react";

export function Header() {
  return (
    <header className="h-14 border-b border-gray-100 bg-white flex items-center justify-between px-6">
      <div className="flex items-center gap-3 bg-gray-50 rounded-lg px-3 py-1.5 w-64">
        <Search size={16} className="text-gray-400" />
        <input
          type="text"
          placeholder="搜索..."
          className="bg-transparent text-sm outline-none w-full text-gray-600 placeholder:text-gray-400"
        />
      </div>
      <div className="flex items-center gap-4">
        <button className="relative p-1.5 rounded-lg hover:bg-gray-50">
          <Bell size={18} className="text-gray-500" />
          <span className="absolute top-0.5 right-0.5 w-2 h-2 bg-red-500 rounded-full" />
        </button>
        <div className="w-8 h-8 rounded-full bg-gray-900 text-white flex items-center justify-center text-sm font-medium">
          U
        </div>
      </div>
    </header>
  );
}
