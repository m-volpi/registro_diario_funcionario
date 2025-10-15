SELECT 
  fl.*,
  F_DIC_PES_NOME(fl.cd_funcionario) AS nm_funcionario
FROM (
  SELECT DISTINCT cd_funcionario
  FROM public.vr_cdf_funloc
) funcs
CROSS JOIN LATERAL (
  SELECT *
  FROM public.vr_cdf_funloc fl2
  WHERE fl2.cd_funcionario = funcs.cd_funcionario
  ORDER BY fl2.dt_cadastro DESC
  LIMIT 1
) fl
ORDER BY fl.cd_funcionario;
