export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">设置</h1>
      <div className="bg-white rounded-xl border border-gray-100 p-6 max-w-lg">
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700">API 密钥</label>
            <input type="password" className="mt-1 w-full px-3 py-2 border border-gray-200 rounded-lg text-sm" value="sk-***" readOnly />
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700">模型</label>
            <input className="mt-1 w-full px-3 py-2 border border-gray-200 rounded-lg text-sm" value="DeepSeek V4pro" readOnly />
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700">接口地址</label>
            <input className="mt-1 w-full px-3 py-2 border border-gray-200 rounded-lg text-sm" value="https://api.deepseek.com" readOnly />
          </div>
        </div>
      </div>
    </div>
  );
}
