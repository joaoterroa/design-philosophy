const fs=require('node:fs'),assert=require('node:assert/strict');
const path=require('node:path');const app=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(app,'tokens.css'),'utf8');
const styles=fs.readFileSync(path.join(app,'styles.css'),'utf8');
const html=fs.readFileSync(path.join(app,'index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const split=tokens.indexOf(':root[data-theme="dark"]');
const light=vars(tokens.slice(0,split)),dark=vars(tokens.slice(split));
assert.deepEqual(styles.match(/#[\da-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[],[],'literal color outside tokens');
for(const prop of ['font-size','border-radius','box-shadow','transition-duration']){
 const values=[...styles.matchAll(new RegExp(prop+':([^;}]+)','g'))].map(m=>m[1].trim());
 assert.deepEqual(values.filter(v=>!v.startsWith('var(')),[],prop+' must use tokens');
}
const componentCss=styles.replace(/@media\s*\([^)]*\)/g,'');
assert.deepEqual(componentCss.match(/(?<![\w-])(?:\d*\.)?\d+(?:px|rem|ms)\b/g)||[],[],'literal dimensions outside tokens (media thresholds exempt)');
const colors=Object.keys(light).filter(k=>light[k].startsWith('#'));
assert.deepEqual(colors.filter(k=>!(k in dark)),[],'dark color parity');
assert(html.indexOf('tokens.css')<html.indexOf('styles.css'),'token wiring');
const lum=hex=>{let v=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);return .2126*v[0]+.7152*v[1]+.0722*v[2]};
const contrast=(a,b)=>{const x=[lum(a),lum(b)].sort((a,b)=>b-a);return (x[0]+.05)/(x[1]+.05)};
const pairs=[['fg','bg'],['fg','surface'],['muted','bg'],['muted','surface'],['accent','bg'],['accent','surface'],['on-accent','accent'],['error','bg'],['error','error-bg'],['success','success-bg'],['focus','bg'],['input-line','surface']];
const report={};
for(const [theme,t] of [['light',light],['dark',{...light,...dark}]]){report[theme]={};for(const [fg,bg]of pairs){const r=contrast(t[fg],t[bg]);const target=['focus','input-line'].includes(fg)?3:4.5;assert(r>=target,`${theme} ${fg}/${bg}: ${r}`);report[theme][`${fg}/${bg}`]=+r.toFixed(2);}}
assert.equal(fs.readFileSync(path.resolve(app,'../../fixtures.js'),'utf8'),fs.readFileSync(path.join(app,'fixtures.js'),'utf8'),'fixture copy unchanged');
fs.writeFileSync(path.join(__dirname,'contrast.json'),JSON.stringify(report,null,2));
console.log('PASS: token use, theme parity, wiring, contrast pairs, fixture integrity');
