const fs=require('fs'),assert=require('assert/strict'),path=require('path');
const root=path.resolve(__dirname,'..'),tokens=fs.readFileSync(path.join(root,'app/tokens.css'),'utf8'),styles=fs.readFileSync(path.join(root,'app/app.css'),'utf8').replace(/\/\*[\s\S]*?\*\//g,''),html=fs.readFileSync(path.join(root,'app/index.html'),'utf8');
const vars=css=>Object.fromEntries([...css.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const blocks=[...tokens.matchAll(/([^{}]+)\{([^{}]*)\}/g)];
const get=selector=>vars(blocks.find(m=>m[1].trim().endsWith(selector))[2]);
const light=get(':root'),dark={...light,...get(':root[data-theme="dark"]')},bankLight={...light,...get('body.bank')},bankDark={...dark,...get('[data-theme="dark"] body.bank')};
const luminance=hex=>{const c=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2]};
const ratio=(a,b)=>{const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
assert.equal((styles.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[]).length,0,'literal colour outside tokens');
for(const m of styles.matchAll(/(?:font-size|border-radius|box-shadow):\s*([^;}]+)/g))assert.ok(m[1].startsWith('var(')||m[1]==='inherit',`untokenised visual value: ${m[0]}`);
for(const [k,v] of Object.entries(light))if(/^#[0-9a-f]{6,8}$/i.test(v))assert.ok(k in get(':root[data-theme="dark"]'),`missing dark token ${k}`);
assert.ok(html.indexOf('tokens.css')<html.indexOf('app.css'),'token stylesheet must load first');
const checks=[];
for(const [name,t] of Object.entries({light,dark,bankLight,bankDark})){
 for(const fg of ['fg','muted','accent','good','warn','danger'])for(const bg of ['bg','surface','soft']){const n=ratio(t[fg],t[bg]);assert.ok(n>=4.5,`${name}: ${fg}/${bg} = ${n}`);checks.push({theme:name,pair:`${fg}/${bg}`,ratio:+n.toFixed(2)});}
 for(const [fg,bg] of [['on-accent','accent'],['good','good-soft'],['warn','warn-soft'],['danger','danger-soft']]){const n=ratio(t[fg],t[bg]);assert.ok(n>=4.5,`${name}: ${fg}/${bg} = ${n}`);checks.push({theme:name,pair:`${fg}/${bg}`,ratio:+n.toFixed(2)});}
 assert.ok(ratio(t.muted,t.track)>=3,`${name}: activity bar contrast`);
}
assert.equal(fs.readFileSync(path.join(root,'app/fixtures.js'),'utf8'),fs.readFileSync(path.join(root,'../fixtures.js'),'utf8'),'fixture must remain exact');
fs.writeFileSync(path.join(__dirname,'contrast-results.json'),JSON.stringify({checks,minimum:Math.min(...checks.map(c=>c.ratio)),passed:true},null,2));
console.log(`Tokens, theme parity, fixture integrity and ${checks.length} contrast pairs passed. Minimum ${Math.min(...checks.map(c=>c.ratio))}:1.`);
