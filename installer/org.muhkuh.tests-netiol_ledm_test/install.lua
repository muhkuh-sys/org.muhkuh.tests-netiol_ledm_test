local t = ...

--t:install('doc/',  '${install_doc}/')
t:install('netx/', '${install_base}/netx/')
t:install('lua/',  '${install_lua_path}/')
t:install('tcl/',  '${install_base}/')

return true
