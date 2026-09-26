async function currentUser(){const {data,error}=await window.sb.auth.getUser();if(error){console.error("Supabase getUser:",error);return null}return data.user||null}
async function currentProfile(){const u=await currentUser();if(!u)return null;const {data,error}=await window.sb.from("perfis").select("id,nome,email,perfil,ativo").eq("id",u.id).maybeSingle();if(error)console.error("Supabase perfil:",error);if(data)return data;return {id:u.id,nome:(u.user_metadata&&u.user_metadata.nome)||"",email:u.email,perfil:"usuario",ativo:true,perfil_pendente:true}}
async function signIn(email,password){return window.sb.auth.signInWithPassword({email,password})}
async function updatePassword(password){return window.sb.auth.updateUser({password})}
async function signOut(){await window.sb.auth.signOut();location.href="./index.html"}
function isRecovery(){return location.hash.includes("type=recovery")||new URLSearchParams(location.search).get("type")==="recovery"}
window.CBAuth={currentUser,currentProfile,signIn,signOut,updatePassword,isRecovery};