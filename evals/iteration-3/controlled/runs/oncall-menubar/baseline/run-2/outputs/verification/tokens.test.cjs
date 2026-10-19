const fs=require('node:fs');const assert=require('node:assert/strict');const path=require('node:path');
const base=path.join(__dirname,'../app');
const css=fs.readFileSync(path.join(base,'tokens.css'),'utf8');
const app=fs.readFileSync(path.join(base,'app.css'),'utf8');
const html=fs.readFileSync(path.join(base,'index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const [lightBlock,darkBlock]=css.split(':root[data-theme="dark"]');const light=vars(lightBlock),dark={...light,...vars(darkBlock)};
const luminance=h=>{const a=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);return a[0]*.2126+a[1]*.7152+a[2]*.0722;};
const contrast=(a,b)=>{let x=luminance(a),y=luminance(b);return(Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
assert(!/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/i.test(app),'Literal color outside tokens');
for(const prop of ['font-size','border-radius','box-shadow','transition-duration']){for(const match of app.matchAll(new RegExp(prop+':([^;}]+)','g'))){assert(/var\(|none/.test(match[1]),`Literal ${prop}: ${match[1]}`);}}
for(const key of Object.keys(light).filter(k=>/^#/.test(light[k])))assert(key in vars(darkBlock),'Missing dark token '+key);
for(const [theme,t] of Object.entries({light,dark})){
 for(const fg of ['fg','muted'])for(const bg of ['bg','surface','field'])assert(contrast(t[fg],t[bg])>=4.5,`${theme} ${fg}/${bg} ${contrast(t[fg],t[bg])}`);
 for(const bg of ['bg','field'])assert(contrast(t['control-line'],t[bg])>=3,`${theme} control border/${bg}`);
 for(const [fg,bg] of [['accent','bg'],['accent','surface'],['accent','accent-tint'],['on-accent','accent'],['caution','bg'],['caution','caution-tint'],['focus','bg']])assert(contrast(t[fg],t[bg])>=4.5,`${theme} ${fg}/${bg} ${contrast(t[fg],t[bg])}`);
}
assert(html.indexOf('tokens.css')<html.indexOf('app.css'),'Tokens must load first');
assert.equal(fs.readFileSync(path.join(base,'fixtures.js'),'utf8'),fs.readFileSync(path.join(base,'../../fixtures.js'),'utf8'),'Fixture copy changed');
console.log('PASS: token usage, theme parity, text/focus contrast, stylesheet wiring, fixture integrity.');
