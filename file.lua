local toolbar = plugin:CreateToolbar("OmniDirection")
local https = game:GetService("HttpService")
local pluginButton = toolbar:CreateButton(
	"Insert Script", --Text that will appear below button
	"Button to insert a script", --Text that will appear if you hover your mouse on button
	"rbxassetid://8740888472")

local widgetInfo = DockWidgetPluginGuiInfo.new(
	Enum.InitialDockState.Float, -- Widget will be initialized in floating panel
	true, -- Widget will be initially enabled
	false, -- Don't override the previous enabled state
	200, -- Default width of the floating window
	300, -- Default height of the floating window
	150, -- Minimum width of the floating window (optional)
	150 -- Minimum height of the floating window (optional)
)

pluginButton.Click:Connect(function()
	local localhost = "http://localhost:5000"
	local  https = game:GetService("HttpService")
	local data = https:GetAsync("http://localhost:5000",true)


	for _,lua in game.ServerScriptService:GetChildren() do
		local extension = lua.ClassName
		if extension == "Script" then
			local d = {
				data=lua.Source
			}
			d=https:JSONEncode(d)
			https:PostAsync(localhost,d)
		end
	end



	
end)