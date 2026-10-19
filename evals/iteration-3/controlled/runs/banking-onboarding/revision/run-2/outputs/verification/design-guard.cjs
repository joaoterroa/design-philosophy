const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'../app'),tokens=fs.readFileSync(path.join(root,'tokens.css'),'utf8'),styles=fs.readFileSync(path.join(root,'app.css'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const split=tokens.indexOf(':root[data-theme="dark"]'),light=vars(tokens.slice(0,split)),darkVars=vars(tokens.slice(split)),dark={...light,...darkVars};
assert(!/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/i.test(styles),'Literal colour outside tokens');
for(const prop of ['font-size','border-radius','box-shadow','transition-duration'])for(const match of styles.matchAll(new RegExp(prop+':([^;}]+)','g')))assert(match[1].includes('var('),prop+' must use tokens');
for(const m of styles.matchAll(/var\(--([\w-]+)\)/g))assert(m[1] in light,'Undefined token '+m[1]);
for(const [k,v] of Object.entries(light))if(/^#/.test(v))assert(k in darkVars,'Missing dark token '+k);
assert.deepEqual(Object.keys(darkVars).sort(),Object.entries(light).filter(([k,v])=>/^#/.test(v)||k==='shadow').map(([k])=>k).sort());
const lum=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4).reduce((a,c,i)=>a+c*[.2126,.7152,.0722][i],0);
const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const report=[];
for(const [theme,t]of Object.entries({light,dark})){
 for(const fg of ['fg','muted','primary'])for(const bg of ['bg','surface','tint']){const r=ratio(t[fg],t[bg]);assert(r>=4.5,`${theme}: ${fg}/${bg} ${r}`);report.push({theme,pair:fg+'/'+bg,ratio:+r.toFixed(2),minimum:4.5});}
 for(const [fg,bg,min]of [['on-primary','primary',4.5],['error','bg',4.5],['error','surface',4.5],['error','error-bg',4.5],['input-line','surface',3],['focus','bg',3],['focus','surface',3],['focus','tint',3]]){const r=ratio(t[fg],t[bg]);assert(r>=min,`${theme}: ${fg}/${bg} ${r}`);report.push({theme,pair:fg+'/'+bg,ratio:+r.toFixed(2),minimum:min});}
}
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');assert(html.indexOf('tokens.css')<html.indexOf('app.css'));
assert(fs.readFileSync(path.join(root,'fixtures.js'),'utf8')===fs.readFileSync(path.resolve(__dirname,'../../fixtures.js'),'utf8'),'Fixture changed');
fs.writeFileSync(path.join(__dirname,'contrast.json'),JSON.stringify(report,null,2));
console.log(`Design guard passed: token wiring/parity, unchanged fixtures, ${report.length} contrast pairs. Minimum text ratio: ${Math.min(...report.filter(x=>x.minimum===4.5).map(x=>x.ratio))}:1`);
