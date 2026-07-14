export default function KnowledgePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">知识库</h1>
      <div className="grid grid-cols-3 gap-4">
        {["简历知识库", "岗位知识库", "面试题库"].map((name) => (
          <div key={name} className="bg-white rounded-xl border border-gray-100 p-5">
            <h3 className="text-sm font-semibold text-gray-900">{name}</h3>
            <p className="text-xs text-gray-500 mt-1">ChromaDB 向量集合</p>
          </div>
        ))}
      </div>
    </div>
  );
}
