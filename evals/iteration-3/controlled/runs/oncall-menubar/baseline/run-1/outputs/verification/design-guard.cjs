/* Offline token, parity and contrast guard. Run: node outputs/verification/design-guard.cjs */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(root,'tokens.css'),'utf8');
const css=fs.readFileSync(path.join(root,'app.css'),'utf8').replace(/\/\*[\s\S]*?\*\//g,'');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const light=vars(tokens.slice(0,tokens.indexOf(':root[data-theme="dark"]')));
const dark=vars(tokens.slice(tokens.indexOf(':root[data-theme="dark"]'),tokens.indexOf('@media')));
const system=vars(tokens.slice(tokens.indexOf('@media')));
const colorKeys=Object.keys(light).filter(k=>/^#[a-f0-9]{6}$/i.test(light[k]));
assert.deepEqual(colorKeys.filter(k=>!dark[k]),[],'Missing dark colour tokens');
assert.deepEqual(dark,system,'System and explicit dark themes differ');
assert.deepEqual(css.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[],[],'Literal colours in components');
for(const prop of ['font-size','border-radius','box-shadow','font-weight','letter-spacing']) {
 for(const m of css.matchAll(new RegExp('(?:^|[;{])'+prop+':([^;}]+)','g')))
 assert.ok(/^var\(--|^inherit$/.test(m[1]),`Non-token ${prop}: ${m[1]}`);
}
for(const m of css.matchAll(/var\(--([\w-]+)/g))assert.ok(m[1] in light,`Undefined token: ${m[1]}`);
assert.ok(html.indexOf('tokens.css')<html.indexOf('app.css'),'Token stylesheet must load first');
const lum=hex=>[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
const ratio=(a,b)=>{let x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const pairs=[...['bg','surface','soft','accent-soft'].flatMap(b=>['fg','muted'].map(f=>[f,b,4.5])),['accent','accent-soft',4.5],['accent','bg',4.5],['on-accent','accent',4.5],['caution','caution-soft',4.5],['focus','bg',3],['focus','surface',3],['accent','line',3]];
const report=[];
for(const [theme,t] of [['light',light],['dark',{...light,...dark}]])for(const [fg,bg,min] of pairs){const actual=ratio(t[fg],t[bg]);assert.ok(actual>=min,`${theme} ${fg}/${bg} contrast ${actual.toFixed(2)} < ${min}`);report.push({theme,fg,bg,ratio:+actual.toFixed(2),minimum:min})}
fs.writeFileSync(path.join(__dirname,'contrast.json'),JSON.stringify(report,null,2));
console.log(`PASS: tokens wired, no component colour/type/radius/shadow literals, theme parity, ${report.length} contrast pairs.`);
