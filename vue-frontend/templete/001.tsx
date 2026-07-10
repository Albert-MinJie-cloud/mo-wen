import React from "react";
import {
  ArrowRight,
  Sparkles,
  TrendingUp,
  Zap,
  Layers,
  CheckCircle2,
  ChevronRight,
} from "lucide-react";

function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <svg
        width="28"
        height="28"
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect width="40" height="40" rx="10" fill="#18181B" />
        <rect x="18" y="9" width="4" height="4" rx="1" fill="#06B6D4" />
        <path
          d="M10 17H30"
          stroke="#FFFFFF"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
        <path
          d="M20 17L12 31"
          stroke="#FFFFFF"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
        <path
          d="M16 24L28 31"
          stroke="#3B82F6"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
      </svg>
      <span className="text-lg font-bold tracking-tight text-white">
        墨文 <span className="font-normal text-neutral-400">Mo-Wen</span>
      </span>
    </div>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-[#09090B] text-neutral-300 font-sans selection:bg-cyan-500/30">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 bg-[#09090B]/80 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Logo />
          <div className="hidden md:flex items-center gap-8 text-sm font-medium">
            <a
              href="#features"
              className="text-neutral-400 hover:text-white transition-colors"
            >
              核心功能
            </a>
            <a
              href="#use-cases"
              className="text-neutral-400 hover:text-white transition-colors"
            >
              应用场景
            </a>
            <a
              href="#pricing"
              className="text-neutral-400 hover:text-white transition-colors"
            >
              价格方案
            </a>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-sm font-medium text-neutral-300 hover:text-white transition-colors hidden sm:block">
              登录
            </button>
            <button className="text-sm font-medium bg-white text-black hover:bg-neutral-200 px-5 py-2.5 rounded-full transition-all flex items-center gap-2">
              免费开始
            </button>
          </div>
        </div>
      </nav>

      <main>
        {/* Hero Section */}
        <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden">
          {/* Background Glow */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-blue-600/20 blur-[120px] rounded-full pointer-events-none"></div>

          <div className="max-w-7xl mx-auto px-6 relative z-10 text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-sm text-cyan-400 font-medium mb-8">
              <Sparkles className="w-4 h-4" />
              <span>新一代 AI 爆文写作引擎已上线</span>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold text-white tracking-tight mb-8 text-balance leading-tight">
              重塑爆款逻辑，
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
                让灵感引爆全网。
              </span>
            </h1>
            <p className="text-lg md:text-xl text-neutral-400 max-w-2xl mx-auto mb-10 text-balance leading-relaxed">
              墨文 (Mo-Wen)
              深度解析小红书、公众号、头条等平台爆款基因。只需输入核心观点，AI
              即刻生成自带流量密码的高质量新媒体文章。
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button className="w-full sm:w-auto px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-neutral-200 transition-colors flex items-center justify-center gap-2">
                立即创作爆款
              </button>
              <button className="w-full sm:w-auto px-8 py-4 bg-white/5 text-white border border-white/10 rounded-full font-semibold text-lg hover:bg-white/10 transition-colors flex items-center justify-center gap-2">
                查看案例 <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </section>

        {/* Mockup Section */}
        <section className="max-w-6xl mx-auto px-6 pb-24 relative z-10">
          <div className="rounded-2xl border border-white/10 bg-[#121214] shadow-2xl overflow-hidden ring-1 ring-white/5">
            {/* Editor Header */}
            <div className="h-12 border-b border-white/5 flex items-center px-4 gap-2 bg-[#09090B]">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
              </div>
              <div className="ml-4 flex-1 text-center text-xs font-medium text-neutral-500">
                mowen-editor.app
              </div>
            </div>
            {/* Editor Body */}
            <div className="flex flex-col md:flex-row h-auto md:h-[500px]">
              {/* Sidebar */}
              <div className="w-full md:w-64 border-b md:border-b-0 md:border-r border-white/5 bg-[#0e0e11] p-5 flex flex-col gap-6">
                <div className="space-y-3">
                  <div className="text-xs font-semibold text-neutral-500 uppercase tracking-wider">
                    创作配置
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs text-neutral-400 ml-1">
                      目标平台
                    </label>
                    <div className="px-3 py-2 bg-white/5 rounded-lg text-sm text-white flex items-center justify-between border border-white/10">
                      小红书{" "}
                      <ChevronRight className="w-4 h-4 text-neutral-500" />
                    </div>
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs text-neutral-400 ml-1">
                      爆款风格
                    </label>
                    <div className="px-3 py-2 bg-transparent hover:bg-white/5 rounded-lg text-sm text-neutral-300 flex items-center justify-between border border-transparent hover:border-white/5 transition-colors cursor-pointer">
                      强烈共鸣 / 痛点挖掘
                    </div>
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs text-neutral-400 ml-1">
                      字数限制
                    </label>
                    <div className="px-3 py-2 bg-transparent hover:bg-white/5 rounded-lg text-sm text-neutral-300 flex items-center justify-between border border-transparent hover:border-white/5 transition-colors cursor-pointer">
                      500 - 800 字
                    </div>
                  </div>
                </div>

                <div className="mt-auto">
                  <button className="w-full py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg text-sm font-medium flex items-center justify-center gap-2 hover:opacity-90 transition-opacity">
                    <Zap className="w-4 h-4" /> 生成爆款文案
                  </button>
                </div>
              </div>
              {/* Main Canvas */}
              <div className="flex-1 p-6 md:p-10 bg-[#121214] overflow-y-auto relative">
                <div className="max-w-2xl mx-auto">
                  <h3 className="text-2xl md:text-3xl font-bold text-white mb-6 leading-snug tracking-tight">
                    那些年薪百万的年轻人，都有这3个反直觉的习惯...
                  </h3>
                  <div className="space-y-5 text-neutral-400 leading-relaxed text-[15px]">
                    <p className="flex items-start gap-3">
                      <span className="mt-2 w-1.5 h-1.5 rounded-full bg-cyan-500 flex-shrink-0 shadow-[0_0_8px_rgba(6,182,212,0.8)]"></span>
                      <span>
                        在这个充满焦虑的时代，我们总是习惯于向外寻找答案。但真正的高手，往往都是在向内探索。
                      </span>
                    </p>
                    <p className="flex items-start gap-3">
                      <span className="mt-2 w-1.5 h-1.5 rounded-full bg-cyan-500 flex-shrink-0 shadow-[0_0_8px_rgba(6,182,212,0.8)]"></span>
                      <span>
                        今天分享的这三个习惯，可能会颠覆你以往的认知，但这正是拉开人与人差距的核心秘密。尤其是第三个，99%的人都在做错。
                      </span>
                    </p>

                    <div className="p-4 mt-8 bg-blue-500/10 border border-blue-500/20 rounded-xl relative overflow-hidden group">
                      <div className="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
                      <p className="text-sm font-medium text-blue-400 flex items-center gap-2 mb-2">
                        <Sparkles className="w-4 h-4" /> AI 留存率优化建议
                      </p>
                      <p className="text-sm text-neutral-300">
                        此处建议插入一个真实的个人职场困境案例（如：25岁遭遇职业瓶颈）。根据数据大盘分析，这能将前3秒的读者流失率降低
                        30%，大幅提升完播和互动率。
                      </p>
                      <div className="mt-3 flex gap-2">
                        <button className="text-xs bg-blue-500/20 text-blue-300 px-3 py-1.5 rounded-md hover:bg-blue-500/30 transition-colors">
                          采纳并生成案例
                        </button>
                        <button className="text-xs bg-white/5 text-neutral-400 px-3 py-1.5 rounded-md hover:bg-white/10 transition-colors">
                          忽略
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section
          id="features"
          className="py-24 bg-[#0e0e11] border-t border-white/5 relative"
        >
          <div className="absolute top-0 inset-x-0 h-px w-full bg-gradient-to-r from-transparent via-cyan-500/20 to-transparent"></div>
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                为什么创作者都在用墨文？
              </h2>
              <p className="text-neutral-400 max-w-2xl mx-auto text-lg">
                不仅仅是文字拼接，更是爆款逻辑的深度复制与二次创新。
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="p-8 rounded-2xl bg-[#121214] border border-white/5 hover:border-white/10 transition-colors group">
                <div className="w-12 h-12 rounded-xl bg-cyan-500/10 flex items-center justify-center text-cyan-400 mb-6 group-hover:scale-110 transition-transform">
                  <TrendingUp className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  爆款基因深度解析
                </h3>
                <p className="text-neutral-400 leading-relaxed text-sm">
                  内置千万级爆文数据库，AI深度学习爆款标题、开头留存、情绪推高及引导互动结构，让你的文章自带网感。
                </p>
              </div>
              <div className="p-8 rounded-2xl bg-[#121214] border border-white/5 hover:border-white/10 transition-colors group">
                <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-400 mb-6 group-hover:scale-110 transition-transform">
                  <Layers className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  多平台风格自适应
                </h3>
                <p className="text-neutral-400 leading-relaxed text-sm">
                  小红书的“情绪价值”、公众号的“深度干货”、头条的“信息差”，一键切换，完美适配各平台调性与排版。
                </p>
              </div>
              <div className="p-8 rounded-2xl bg-[#121214] border border-white/5 hover:border-white/10 transition-colors group">
                <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-400 mb-6 group-hover:scale-110 transition-transform">
                  <Zap className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  实时热点追踪融合
                </h3>
                <p className="text-neutral-400 leading-relaxed text-sm">
                  接入全网热搜榜单，创作时自动建议融合当下热点词汇与话题，轻松蹭上流量快车，提升搜索曝光率。
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-[#09090B] to-[#0a1122]"></div>
          <div className="max-w-4xl mx-auto px-6 relative z-10 text-center">
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
              准备好创作你的下一篇 10w+ 了吗？
            </h2>
            <p className="text-xl text-neutral-400 mb-10">
              加入 10,000+ 创作者的行列，释放 AI 的创作潜能。
            </p>
            <button className="px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-neutral-200 transition-colors flex items-center justify-center gap-2 mx-auto">
              立即免费体验 <ArrowRight className="w-5 h-5" />
            </button>
            <div className="mt-8 flex items-center justify-center gap-6 text-sm text-neutral-500">
              <span className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-500" /> 无需信用卡
              </span>
              <span className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-500" /> 注册即送
                5000 算力
              </span>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="py-12 border-t border-white/10 bg-[#09090B] text-neutral-500 text-sm">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-3">
            <Logo />
            <span className="ml-2">© 2026 Mo-Wen AI. All rights reserved.</span>
          </div>
          <div className="flex gap-6">
            <a href="#" className="hover:text-white transition-colors">
              服务条款
            </a>
            <a href="#" className="hover:text-white transition-colors">
              隐私政策
            </a>
            <a href="#" className="hover:text-white transition-colors">
              联系我们
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
