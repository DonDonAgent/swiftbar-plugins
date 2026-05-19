#!/bin/bash
KEY=$(grep _DEEPSEEK_KEY "$HOME/.zprofile" 2>/dev/null | head -1 | sed 's/.*="//;s/"//')
B=$(curl -s --max-time 5 "https://api.deepseek.com/user/balance" -H "Authorization: Bearer $KEY" | /usr/bin/python3 -c "import sys,json;print(sum(float(i['total_balance']) for i in json.load(sys.stdin).get('balance_infos',[])))")
echo "DS: \$${B:-?}"
echo "---"
echo "💰 \$${B:-unknown}"
echo "---"
echo "🔄 Refresh | refresh=true"
