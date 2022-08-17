-- Client discordia
-- Author: Kidcraft18
-- Linguagem: Lua

local discordia = require('discordia')
local settings = require("settings")
local bot = discordia.Client()
local comando_lista = {}
local evento_lista = {}

for i,v in pairs(settings.Comandos) do
	local comando = require('../comandos/' .. v)
	table.insert(comando_lista, {
		name = comando.name,
		aliases = comando.aliases,
		run = comando.commandRun
	})
end

function commandRun(msg)
	local args = string.split(msg.content, ' ')
	local comando = string.gsub(args[1], '!', '')

	args = table.slice(args, 2)
	comando = string.lower(comando)

	local comando_objeto

	for i, v in pairs(comando_lista) do
		if string.lower(v.name) == comando or string.lower(v.alias) == comando then
			comando_objeto = v
		end
	end

	if(comando_objeto) then
		comando_objeto.run(bot, msg, args, {
			comandos = comando_lista,
			prefix = "!"
		});
	end
end

bot:run('Bot '.. settings.Token)