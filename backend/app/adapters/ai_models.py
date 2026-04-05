from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx


class AIModelAdapter(ABC):
    """AI模型适配器基类"""

    def __init__(self, api_key: Optional[str] = None, api_endpoint: Optional[str] = None, model_id: Optional[str] = None):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.model_id = model_id

    @abstractmethod
    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        """
        分析内容，返回实体和关系

        Args:
            content: 内容（文字或base64编码的图片）
            content_type: 内容类型 (text/image/video)
            prompt: 提示词

        Returns:
            {"entities": [...], "relations": [...]}
        """
        pass


class ClaudeAdapter(AIModelAdapter):
    """Claude 适配器"""

    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=self.api_key)

        messages = []

        if content_type == "text":
            messages.append({
                "role": "user",
                "content": f"{prompt}\n\n内容：\n{content}"
            })
        else:
            # 图片/视频，假设content是base64
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": content
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
            })

        response = await client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=messages
        )

        # 解析返回结果
        import json
        text = response.content[0].text
        try:
            # 尝试提取JSON
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
            return {"entities": [], "relations": []}
        except:
            return {"entities": [], "relations": []}


class OpenAIAdapter(AIModelAdapter):
    """OpenAI GPT-4V 适配器"""

    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)

        messages = []

        if content_type == "text":
            messages.append({
                "role": "user",
                "content": f"{prompt}\n\n内容：\n{content}"
            })
        else:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{content}"
                        }
                    }
                ]
            })

        response = await client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=4096
        )

        import json
        text = response.choices[0].message.content
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
            return {"entities": [], "relations": []}
        except:
            return {"entities": [], "relations": []}


class GeminiAdapter(AIModelAdapter):
    """Google Gemini 适配器"""

    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        import google.generativeai as genai

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel('gemini-pro-vision')

        if content_type == "text":
            response = await model.generate_content_async(f"{prompt}\n\n内容：\n{content}")
        else:
            import base64
            from PIL import Image
            import io
            # 解码base64图片
            image_data = base64.b64decode(content)
            image = Image.open(io.BytesIO(image_data))
            response = await model.generate_content_async([prompt, image])

        import json
        text = response.text
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
            return {"entities": [], "relations": []}
        except:
            return {"entities": [], "relations": []}


class GLMAdapter(AIModelAdapter):
    """智谱AI GLM-4V 适配器"""

    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        from zhipuai import ZhipuAI

        client = ZhipuAI(api_key=self.api_key)

        messages = []
        if content_type == "text":
            messages.append({
                "role": "user",
                "content": f"{prompt}\n\n内容：\n{content}"
            })
        else:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{content}"}
                    }
                ]
            })

        response = client.chat.completions.create(
            model="glm-4v",
            messages=messages
        )

        import json
        text = response.choices[0].message.content
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
            return {"entities": [], "relations": []}
        except:
            return {"entities": [], "relations": []}


class QwenAdapter(AIModelAdapter):
    """阿里云 Qwen 适配器（支持百炼平台 OpenAI 兼容格式）"""

    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        import json

        # 使用配置的模型名称，或默认值
        model = self.model_id or "qwen-vl-max"

        # 如果配置了自定义端点，使用 OpenAI 兼容格式
        if self.api_endpoint:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.api_endpoint
            )

            messages = []
            if content_type == "text":
                messages.append({
                    "role": "user",
                    "content": f"{prompt}\n\n内容：\n{content}"
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{content}"}
                        }
                    ]
                })

            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=4096
            )

            text = response.choices[0].message.content or ""
        else:
            # 使用 dashscope SDK
            import asyncio
            import dashscope
            from dashscope import MultiModalConversation

            dashscope.api_key = self.api_key

            messages = []
            if content_type == "text":
                messages.append({
                    "role": "user",
                    "content": [{"text": f"{prompt}\n\n内容：\n{content}"}]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [
                        {"image": f"data:image/png;base64,{content}"},
                        {"text": prompt}
                    ]
                })

            def _call_api():
                return MultiModalConversation.call(
                    model=model,
                    messages=messages
                )

            response = await asyncio.to_thread(_call_api)

            if response.status_code != 200:
                error_msg = response.message if hasattr(response, 'message') else '未知错误'
                raise Exception(f"Qwen API 错误: {error_msg}")

            try:
                text = response.output.choices[0].message.content[0]["text"]
            except (KeyError, IndexError, TypeError) as e:
                raise Exception(f"Qwen API 响应格式错误: {e}")

        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
            return {"entities": [], "relations": []}
        except json.JSONDecodeError:
            return {"entities": [], "relations": []}


class DeepSeekAdapter(AIModelAdapter):
    """DeepSeek 适配器（兼容OpenAI格式）"""

    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.api_endpoint or "https://api.deepseek.com/v1"
        )

        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "user",
                "content": f"{prompt}\n\n内容：\n{content}"
            }]
        )

        import json
        text = response.choices[0].message.content
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
            return {"entities": [], "relations": []}
        except:
            return {"entities": [], "relations": []}


class LocalModelAdapter(AIModelAdapter):
    """本地模型适配器"""

    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        if not self.api_endpoint:
            raise ValueError("本地模型需要配置 api_endpoint")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_endpoint,
                json={
                    "content": content,
                    "content_type": content_type,
                    "prompt": prompt
                },
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                timeout=120
            )
            response.raise_for_status()
            return response.json()


# 模型工厂
def get_adapter(model_name: str, api_key: Optional[str] = None, api_endpoint: Optional[str] = None, model_id: Optional[str] = None) -> AIModelAdapter:
    adapters = {
        "claude": ClaudeAdapter,
        "openai": OpenAIAdapter,
        "gemini": GeminiAdapter,
        "glm": GLMAdapter,
        "qwen": QwenAdapter,
        "deepseek": DeepSeekAdapter,
        "local": LocalModelAdapter,
    }
    adapter_class = adapters.get(model_name, LocalModelAdapter)
    return adapter_class(api_key=api_key, api_endpoint=api_endpoint, model_id=model_id)


# 默认提示词模板
DEFAULT_PROMPT = """请分析以下内容，提取其中的实体（本体）和它们之间的关系。

内容类型：{content_type}

请按以下JSON格式返回：
{
  "entities": [
    {"name": "实体名称", "type": "类型", "description": "描述"}
  ],
  "relations": [
    {"source": "源实体名称", "target": "目标实体名称", "type": "关系类型", "description": "描述"}
  ]
}

实体类型建议：person(人物)、concept(概念)、process(流程)、object(物体)、event(事件)
关系类型建议：依赖、包含、导致、关联、属于、产生
"""