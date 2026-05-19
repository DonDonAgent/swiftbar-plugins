#!/bin/bash
source ~/.zprofile 2>/dev/null
B=$(curl -s "https://api.deepseek.com/user/balance" -H "Authorization: Bearer $_DEEPSEEK_KEY" | python3 -c "import sys,json;print(sum(float(i['total_balance']) for i in json.load(sys.stdin).get('balance_infos',[])))" 2>/dev/null)
echo "DS: \$${B:-?}"
echo "---"
echo "💰 \$${B:-unknown}"
echo "---"
echo "🔄 Refresh | refresh=true"
