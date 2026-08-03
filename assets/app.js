// ===== 主题切换 =====
function toggleTheme(){
  const cur = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = cur === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  try { localStorage.setItem('abop-theme', next); } catch(e){}
}
(function(){
  let t = 'dark';
  try { t = localStorage.getItem('abop-theme') || 'dark'; } catch(e){}
  document.documentElement.setAttribute('data-theme', t);
})();

// ===== 代码复制 =====
function copyCode(btn){
  const card = btn.closest('.code-card');
  const code = card ? card.querySelector('code') : null;
  if(!code) return;
  const text = code.innerText;
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(()=>{
      btn.textContent = '已复制'; setTimeout(()=>btn.textContent='复制', 1200);
    }).catch(()=>fallbackCopy(text, btn));
  } else { fallbackCopy(text, btn); }
}
function fallbackCopy(text, btn){
  const ta = document.createElement('textarea');
  ta.value = text; document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); btn.textContent='已复制'; setTimeout(()=>btn.textContent='复制',1200);}catch(e){}
  document.body.removeChild(ta);
}

// ===== 通讯录仿真（仅模拟数据，不执行 Python / 不读写真实文件）=====
const simBook = { "李雷":"13800000001", "韩梅梅":"13800000002", "王芳":"13912345678" };
function simLog(s){
  const o = document.getElementById('simOut');
  if(!o) return;
  o.textContent += '\n' + s;
  o.scrollTop = o.scrollHeight;
}
function simAdd(){
  const n = (document.getElementById('cName')||{}).value;
  const p = (document.getElementById('cPhone')||{}).value;
  if(!n || !p){ simLog('! 请输入姓名和电话'); return; }
  if(simBook[n]){ simLog('! 联系人 '+n+' 已存在'); return; }
  simBook[n] = p; simLog('✓ 已添加：'+n+' / '+p);
  document.getElementById('cName').value=''; document.getElementById('cPhone').value='';
}
function simSearch(){
  const n = (document.getElementById('cName')||{}).value;
  if(!n){ simLog('! 请输入要查找的姓名'); return; }
  if(simBook[n]) simLog('🔎 找到：'+n+' -> '+simBook[n]); else simLog('🔎 未找到：'+n);
}
function simDel(){
  const n = (document.getElementById('cName')||{}).value;
  if(!n){ simLog('! 请输入要删除的姓名'); return; }
  if(simBook[n]){ delete simBook[n]; simLog('🗑 已删除：'+n); } else simLog('🗑 联系人不存在：'+n);
}
function simDisplay(){
  const o = document.getElementById('simOut'); if(!o) return;
  o.textContent = 'Name\t\tMobile\n' + '─'.repeat(28);
  Object.keys(simBook).forEach(k=>simLog(k+'\t\t'+simBook[k]));
  simLog('— 共 '+Object.keys(simBook).length+' 条（模拟数据，刷新即重置）');
}
