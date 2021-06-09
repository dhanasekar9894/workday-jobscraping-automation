{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled3.ipynb",
      "provenance": [],
      "authorship_tag": "ABX9TyP/t+bTW1yYGaPDicgL+K4r",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/dhanasekar9894/workday-jobscraping-automation/blob/main/scraper.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 231
        },
        "id": "S8apDmidUAOV",
        "outputId": "2cf5cd51-bd6b-42c7-9932-9df3c69bd9ed"
      },
      "source": [
        "import requests\n",
        "import re\n",
        "import json\n",
        "ses = requests.Session()\n",
        "import pandas as pd\n",
        "\n",
        "class JOBS:\n",
        "\n",
        "    def __init__(self, url=None, filename=None, output=None):\n",
        "        if url is None:\n",
        "            raise TypeError(\"Please enter url from myworkday site!!!\")\n",
        "        self.url = url\n",
        "        self.output = output\n",
        "        self.filename = filename\n",
        "        self.ID = \"efc49a3159bb428ab71e15425e0f4c13\"\n",
        "\n",
        "    def parse(self):\n",
        "        url_parse = {\n",
        "            \"host\":  re.compile(\"(\\w+?[-.].+?)[/]\"),\n",
        "            \"query\":  re.compile(\"\\w?/[^\\/\\s]+\\/?(.*)\"),\n",
        "            \"protocol\": re.compile(\"(\\w+)[:]\")\n",
        "        }\n",
        "        return url_parse\n",
        "\n",
        "    def Regexp(self):\n",
        "        url = JOBS.parse(self)\n",
        "        List = []\n",
        "        for N,R in url.items():\n",
        "            try:\n",
        "                List.append(R.findall(self.url)[0])\n",
        "            except IndexError:\n",
        "                return None\n",
        "        yt = {\n",
        "            \"h\": List[0],\n",
        "            \"q\": List[1]\n",
        "        }\n",
        "        return yt\n",
        "\n",
        "    @property\n",
        "    def Headers(self):\n",
        "        headers = {\n",
        "            \"Accept\": \"application/json,application/xml\",\n",
        "            \"workday-client-manifest-id\": \"mvp\",\n",
        "            \"X-Workday-Client\": \"2021.20.011\",\n",
        "            \"User-Agent\": \"Mozilla/5.0 (Linux; Android 10; SM-J400F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Mobile Safari/537.36\",\n",
        "            \"Content-Type\": \"application/x-www-form-urlencoded\"\n",
        "        }\n",
        "        return headers\n",
        "\n",
        "    def req(self):\n",
        "        title = []\n",
        "        location = []\n",
        "        link = []\n",
        "        date = []\n",
        "        R = []\n",
        "        total = []\n",
        "        dts = self.Regexp()\n",
        "        fo = ses.get(\n",
        "                url=f\"https://%s/{dts['q']}?clientRequestID={self.ID}\"%(dts['h']),\n",
        "                headers=self.Headers\n",
        "            ).json()\n",
        "        total.append(fo)\n",
        "        pagination = fo['body']['children'][0]\n",
        "        sg = re.findall(\"/\\S+searchPagination/\\w+\", re.findall(\"'uri': '/.*Pagination.+'\", str(pagination))[0])[0]\n",
        "\n",
        "        Known_Pages= [50, 100, 150, 200]\n",
        "              \n",
        "        for i in Known_Pages:\n",
        "            ur = f\"https://{dts['h']}{sg}/%s?clientRequestID={self.ID}\" % (i)\n",
        "            tot = ses.get(url=ur, headers=self.Headers)\n",
        "            if not '404' in str(tot.status_code):\n",
        "                total.append(tot.json())\n",
        "\n",
        "        for pages in total:\n",
        "            main = pages['body']['children'][0]['children']\n",
        "            \n",
        "            for items in main:\n",
        "                for dat in items['listItems']:\n",
        "                    title.append(dat['title']['instances'][0]['text'])\n",
        "                    link.append(f\"https://{dts['h']}%s?{dts['q']}={self.ID}\"%(dat['title']['commandLink']))\n",
        "                    R.append(dat['subtitles'][0]['instances'][0]['text'])\n",
        "                    location.append(dat['subtitles'][1]['instances'][0]['text'])\n",
        "                    date.append(dat['subtitles'][2]['instances'][0]['text'])\n",
        "                    \n",
        "\n",
        "#        for desp in link:\n",
        "#            req1 = ses.get(desp, headers=self.Headers).json()\n",
        "#            for t6 in re.findall(\"t':\\s+'(<p><b><span>.*?>)', \", str(req1)):\n",
        "#                description.append(t6)\n",
        "\n",
        "#case 1\n",
        "###     \"e': '(<p>.*</p>)'}, \" some issues in matching\n",
        "\n",
        "#case 2\n",
        "###     \"t':\\s+'(<p><b><span>.*?>)', works & tested on \"https://regex101.com/\"\n",
        "\n",
        "\n",
        "        cx = pd.DataFrame({\n",
        "                \"Job-Tile\": title,\n",
        "                \"R\": R,\n",
        "#                \"Job-Description\": description,\n",
        "                \"Link\": link,\n",
        "                \"Job-Location\": location,\n",
        "                \"Job-Posted\": date,\n",
        "            \n",
        "            })\n",
        "        try:\n",
        "            from time import ctime\n",
        "            if self.output and self.filename is not None:\n",
        "                if self.output.lower() == \"csv\":\n",
        "                    cx.to_csv(f\"{self.filename}.{self.output}\", index=False)\n",
        "                elif self.output.lower() == \"xlsx\":\n",
        "                    cx.to_excel(f\"{self.filename}.{self.output}\", engine='xlsxwriter')\n",
        "            else:\n",
        "                return \"setting default output\"\n",
        "                cx.to_csv(\"Job-Datas-%s.csv\" % (ctime()), index=False)\n",
        "        except IndexError:\n",
        "            return \"try-again\"\n",
        "\n",
        "scraped_contents = JOBS(\n",
        "        url=\"https://brocku.wd3.myworkdayjobs.com/brocku_careers/\",\n",
        "        filename=\"preetii\",\n",
        "        output=\"csv\"\n",
        "    \n",
        ").req()\n",
        "scraped_contents.to_csv(\"./drive/My Drive/preetiii.csv\")\n",
        "\n",
        "scraped_contents\n"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "error",
          "ename": "AttributeError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mAttributeError\u001b[0m                            Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-2-b253fa300eb7>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m    124\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    125\u001b[0m ).req()\n\u001b[0;32m--> 126\u001b[0;31m \u001b[0mscraped_contents\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mto_csv\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"./drive/My Drive/preetiii.csv\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    127\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    128\u001b[0m \u001b[0mscraped_contents\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mAttributeError\u001b[0m: 'NoneType' object has no attribute 'to_csv'"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "krkwjrcCWg0x"
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}