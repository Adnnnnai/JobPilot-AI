export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">工作台</h1>
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "简历", value: "3", icon: "✓" },
          { label: "岗位匹配", value: "12", icon: "💼" },
          { label: "面试题", value: "25", icon: "🎤" },
          { label: "知识库文档", value: "128", icon: "📚" },
        ].map((s) => (
          <div key={s.label} className="bg-white rounded-xl border border-gray-100 p-5">
            <div className="text-2xl mb-1">{s.icon}</div>
            <div className="text-2xl font-bold text-gray-900">{s.value}</div>
            <div className="text-sm text-gray-500">{s.label}</div>
          </div>
        ))}
      </div>
      <div className="bg-white rounded-xl border border-gray-100 p-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-3">快捷操作</h3>
        <div className="flex gap-3">
          <a href="/resume" className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium">上传简历</a>
          <a href="/job" className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium">岗位匹配</a>
          <a href="/interview" className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium">模拟面试</a>
        </div>
      </div>
    </div>
  );
}
