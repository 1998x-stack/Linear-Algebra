(() => {
  "use strict";
  const $ = (s) => document.querySelector(s);
  const eps = 1e-10;
  const clone = A => A.map(r => r.slice());
  const eye = n => Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?1:0));
  const dot = (a,b) => a.reduce((s,x,i)=>s+x*b[i],0);
  const norm = a => Math.sqrt(dot(a,a));
  const transpose = A => A[0].map((_,j)=>A.map(r=>r[j]));
  const mm = (A,B) => A.map(r=>B[0].map((_,j)=>r.reduce((s,x,k)=>s+x*B[k][j],0)));
  const sub = (A,B) => A.map((r,i)=>r.map((x,j)=>x-B[i][j]));
  const maxAbs = A => Math.max(0,...A.flat().map(Math.abs));
  const fmt = x => (Math.abs(x)<5e-11?0:x).toFixed(4);
  const mat = A => A.map(r=>"[ "+r.map(fmt).join(", ")+" ]").join("\n");
  function parse(text){
    const rows=text.trim().split(/\n+/).map(line=>line.trim().split(/[\s,;]+/).map(Number));
    if(rows.length<2||rows.length>3||rows.some(r=>r.length!==rows.length||r.some(x=>!Number.isFinite(x)))) throw new Error("请输入 2×2 或 3×3 的有限实数方阵。");
    return rows;
  }
  function determinant(A){
    const U=clone(A),n=U.length;let det=1,sign=1;
    for(let k=0;k<n;k++){
      let p=k;for(let i=k+1;i<n;i++)if(Math.abs(U[i][k])>Math.abs(U[p][k]))p=i;
      if(Math.abs(U[p][k])<eps)return 0;
      if(p!==k){[U[p],U[k]]=[U[k],U[p]];sign*=-1;}
      const pivot=U[k][k];det*=pivot;
      for(let i=k+1;i<n;i++){const m=U[i][k]/pivot;for(let j=k+1;j<n;j++)U[i][j]-=m*U[k][j];}
    }
    return sign*det;
  }
  function luFactor(A){
    const n=A.length,U=clone(A),L=eye(n),P=eye(n);let swaps=0;
    for(let k=0;k<n;k++){
      let p=k;for(let i=k+1;i<n;i++)if(Math.abs(U[i][k])>Math.abs(U[p][k]))p=i;
      if(Math.abs(U[p][k])<eps)throw new Error("矩阵奇异或数值上缺少非零主元。");
      if(p!==k){[U[p],U[k]]=[U[k],U[p]];[P[p],P[k]]=[P[k],P[p]];for(let j=0;j<k;j++)[L[p][j],L[k][j]]=[L[k][j],L[p][j]];swaps++;}
      for(let i=k+1;i<n;i++){L[i][k]=U[i][k]/U[k][k];for(let j=k;j<n;j++)U[i][j]-=L[i][k]*U[k][j];U[i][k]=0;}
    }
    return {L,U,P,swaps};
  }
  function qrFactor(A){
    const n=A.length,cols=transpose(A),Q=[],R=Array.from({length:n},()=>Array(n).fill(0));
    for(let j=0;j<n;j++){
      let v=cols[j].slice();
      for(let i=0;i<j;i++){R[i][j]=dot(Q[i],v);v=v.map((x,k)=>x-R[i][j]*Q[i][k]);}
      R[j][j]=norm(v);if(R[j][j]<eps)throw new Error("列向量线性相关，QR 的满秩演示不适用。");
      Q.push(v.map(x=>x/R[j][j]));
    }
    return {Q:transpose(Q),R};
  }
  function jacobi(A){
    const D=clone(A),n=D.length,V=eye(n);
    for(let iter=0;iter<100*n*n;iter++){
      let p=0,q=1,big=0;
      for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(Math.abs(D[i][j])>big){big=Math.abs(D[i][j]);p=i;q=j;}
      if(big<1e-12)break;
      const app=D[p][p],aqq=D[q][q],apq=D[p][q];
      const tau=(aqq-app)/(2*apq);
      const t=(tau>=0?1:-1)/(Math.abs(tau)+Math.sqrt(1+tau*tau));
      const c=1/Math.sqrt(1+t*t),s=t*c;
      D[p][p]=app-t*apq;D[q][q]=aqq+t*apq;D[p][q]=0;D[q][p]=0;
      for(let k=0;k<n;k++)if(k!==p&&k!==q){const dkp=D[k][p],dkq=D[k][q];D[k][p]=D[p][k]=c*dkp-s*dkq;D[k][q]=D[q][k]=s*dkp+c*dkq;}
      for(let k=0;k<n;k++){const vkp=V[k][p],vkq=V[k][q];V[k][p]=c*vkp-s*vkq;V[k][q]=s*vkp+c*vkq;}
    }
    return {values:D.map((r,i)=>r[i]),vectors:V};
  }
  function cholesky(A){
    const n=A.length,L=Array.from({length:n},()=>Array(n).fill(0));
    for(let i=0;i<n;i++)for(let j=0;j<=i;j++){
      let s=A[i][j];for(let k=0;k<j;k++)s-=L[i][k]*L[j][k];
      if(i===j){if(s<=eps)throw new Error("存在非正主元；矩阵不是正定矩阵。");L[i][j]=Math.sqrt(s);}
      else L[i][j]=s/L[j][j];
    }
    return L;
  }
  function run(){
    const out=$("#lab-result");
    try{
      const A=parse($("#matrix-input").value),n=A.length,At=transpose(A),det=determinant(A),lines=[];
      lines.push("维度："+n+" × "+n,"det(A) = "+fmt(det),"");
      try{const {L,U,P,swaps}=luFactor(A),res=maxAbs(sub(mm(P,A),mm(L,U)));lines.push("[LU · partial pivoting]","P =\n"+mat(P),"L =\n"+mat(L),"U =\n"+mat(U),"row swaps = "+swaps,"‖PA−LU‖max = "+fmt(res),"");}
      catch(e){lines.push("[LU] 不可用："+e.message,"");}
      try{const {Q,R}=qrFactor(A),orth=maxAbs(sub(mm(transpose(Q),Q),eye(n))),res=maxAbs(sub(mm(Q,R),A));lines.push("[QR · Modified Gram–Schmidt]","Q =\n"+mat(Q),"R =\n"+mat(R),"‖QᵀQ−I‖max = "+fmt(orth),"‖QR−A‖max = "+fmt(res),"");}
      catch(e){lines.push("[QR] 不可用："+e.message,"");}
      const symmetric=maxAbs(sub(A,At))<1e-9;
      if(symmetric){const eig=jacobi(A).values.sort((a,b)=>b-a);lines.push("[对称特征值 · Jacobi]","λ = ["+eig.map(fmt).join(", ")+"]","A≈Aᵀ：通过对称性前提检查","");}
      else lines.push("[对称特征值] 跳过：输入矩阵不是对称矩阵。","");
      if(symmetric){try{const L=cholesky(A);lines.push("[Cholesky] A = LLᵀ","L =\n"+mat(L),"‖LLᵀ−A‖max = "+fmt(maxAbs(sub(mm(L,transpose(L)),A))),"");}catch(e){lines.push("[Cholesky] 不适用："+e.message,"");}}
      else lines.push("[Cholesky] 跳过：标准实数 Cholesky 要求对称正定。","");
      const ata=mm(At,A),sv=jacobi(ata).values.map(v=>Math.sqrt(Math.max(0,v))).sort((a,b)=>b-a);
      lines.push("[SVD · 由 AᵀA 的特征值计算奇异值]","σ = ["+sv.map(fmt).join(", ")+"]","注意：这是 2×2/3×3 教学实现，不是生产级 SVD 算法。");
      out.textContent=lines.join("\n");
    }catch(e){out.textContent="输入错误： "+e.message;}
  }
  $("#run-lab")?.addEventListener("click",run);
  run();
})();