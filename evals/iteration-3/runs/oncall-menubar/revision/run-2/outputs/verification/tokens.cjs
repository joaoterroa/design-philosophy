const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),tokens=fs.readFileSync(path.join(root,'app/tokens.css'),'utf8'),css=fs.readFileSync(path.join(root,'app/app.css'),'utf8').replace(/\/\*[\s\S]*?\*\//g,'');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const split=tokens.indexOf(':root[data-theme="dark"]'),light=vars(tokens.slice(0,split)),overrides=vars(tokens.slice(split)),dark={...light,...overrides};
assert.deepEqual(css.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[],[],'Literal colors outside tokens');
for(const m of css.matchAll(/(?:font-size|border-radius|box-shadow):\s*([^;}]+)/g)) assert.match(m[1],/^var\(/,'Untokenized type, radius or shadow: '+m[0]);
const colorNames=Object.keys(light).filter(k=>/^#[0-9a-f]{6}$/i.test(light[k]));
assert.deepEqual(colorNames.filter(k=>!(k in overrides)),[],'Missing dark color roles');
const luminance=h=>{const c=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722;};
const ratio=(a,b)=>{const x=[luminance(a),luminance(b)].sort((a,b)=>b-a);return (x[0]+.05)/(x[1]+.05);};
const pairs=[...['fg','muted'].flatMap(f=>['bg','surface','soft','bank-bg','bank-soft'].map(b=>[f,b])),['accent','accent-soft'],['on-accent','accent'],['good','good-soft'],['warn','warn-soft'],['danger','danger-soft'],['bank-on','bank-accent'],['bank-accent','bank-bg'],['bank-accent','bank-soft'],['dash-fg','dash-bg'],['dash-muted','dash-bg'],['danger','dash-bg'],['warn','dash-bg'],['good','dash-bg']];
const report=[];
for(const [name,t] of [['light',light],['dark',dark]]) for(const [fg,bg] of pairs){const r=ratio(t[fg],t[bg]);report.push({theme:name,fg,bg,ratio:+r.toFixed(2)});assert.ok(r>=4.5,`${name} ${fg} on ${bg}: ${r.toFixed(2)}`);}
for(const t of [light,dark]) for(const bg of ['surface','bank-bg','soft'])assert.ok(ratio(t['control-line'],t[bg])>=3,`Control boundary on ${bg}`);
const html=fs.readFileSync(path.join(root,'app/index.html'),'utf8');assert.ok(html.indexOf('tokens.css')<html.indexOf('app.css'),'Tokens load first');
assert.equal(fs.readFileSync(path.join(root,'app/fixtures.js'),'utf8'),fs.readFileSync(path.join(root,'../fixtures.js'),'utf8'),'Fixture copy unchanged');
fs.writeFileSync(path.join(root,'verification/contrast.json'),JSON.stringify(report,null,2));
console.log(`PASS: theme parity; token-only color, type, radius and shadow; ${report.length} text contrast pairs >= 4.5:1; controls >=3:1; fixture copy unchanged.`);
