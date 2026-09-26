async function currentUser(){const {data}=await window.sb.auth.getUser();return data.user||null}
async function currentProfile(){const u=await currentUser();if(!u)return null;const {data}=await window.sb.from("perfis").select("id,nome,email,perfil,ativo").eq("id",u.id).single();return data}
async function signIn(email,password){return window.sb.auth.signInWithPassword({email,password})}
async function updatePassword(password){return window.sb.auth.updateUser({password})}
async function signOut(){await window.sb.auth.signOut();location.href="./index.html"}
function isRecovery(){return location.hash.includes("type=recovery")||new URLSearchParams(location.search).get("type")==="recovery"}
window.CBAuth={currentUser,currentProfile,signIn,signOut,updatePassword,isRecovery};