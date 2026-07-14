"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, FileText, Briefcase, Sparkles,
  Mic, BookOpen, Settings, Zap
} from "lucide-react";

const NAV = [
  { href: "/dashboard", label: "工作台", icon: LayoutDashboard },
  { href: "/resume", label: "简历中心", icon: FileText },
  { href: "/job", label: "岗位匹配", icon: Briefcase },
  { href: "/rewrite", label: "简历优化", icon: Sparkles },
  { href: "/interview", label: "模拟面试", icon: Mic },
  { href: "/knowledge", label: "知识库", icon: BookOpen },
  { href: "/workspace", label: "AI 工作区", icon: Zap },
  { href: "/settings", label: "设置", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 bg-white border-r border-gray-100 flex flex-col py-4 px-3">
      <Link href="/dashboard" className="text-lg font-bold text-gray-900 px-3 pb-6">
        JobPilot AI
      </Link>
      <nav className="flex flex-col gap-1">
        {NAV.map((item) => {
          const active = pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                active
                  ? "bg-gray-900 text-white"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              <Icon size={18} />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
