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
            model=self.model_id or "claude-3-opus-20240229",
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
            model=self.model_id or "gpt-4o",
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
        model = genai.GenerativeModel(self.model_id or 'gemini-1.5-pro')

        if content_type == "text":
            response = await model.generate_content_async(f"{prompt}\n\n内容：\n{content}")
        else:
            # 使用官方支持的字典格式传入 base64，避免使用 PIL
            mime_type = "image/jpeg" if content_type == "image" else "video/mp4"
            image_part = {
                "mime_type": mime_type,
                "data": content
            }
            response = await model.generate_content_async([prompt, image_part])

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
            model=self.model_id or "glm-4v",
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
    """阿里云 Qwen 适配器（统一使用 OpenAI 兼容格式，支持所有百炼模型）"""

    # 百炼标准兼容端点（未配置自定义端点时使用）
    DEFAULT_ENDPOINT = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    async def analyze(self, content: str, content_type: str, prompt: str) -> Dict[str, Any]:
        import json
        from openai import AsyncOpenAI

        # 使用自定义端点或默认百炼兼容端点
        # Coding Plan 专用端点: https://coding.dashscope.aliyuncs.com/v1
        # 标准端点:             https://dashscope.aliyuncs.com/compatible-mode/v1
        base_url = self.api_endpoint or self.DEFAULT_ENDPOINT

        # 使用配置的模型名称，或默认值
        # 注意: qwen-coding-plan 是纯文本模型，不支持图片输入
        model = self.model_id or "qwen-plus"

        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=base_url
        )

        messages = []
        if content_type == "text":
            messages.append({
                "role": "user",
                "content": f"{prompt}\n\n内容：\n{content}"
            })
        else:
            # 视觉类模型（qwen-vl-max 等）支持图片；纯文本模型会报错
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

        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=4096
            )
            text = response.choices[0].message.content or ""
        except Exception as e:
            error_str = str(e)
            # 提供更友好的错误提示
            if "model" in error_str.lower() or "404" in error_str:
                raise Exception(
                    f"模型 '{model}' 不存在或无访问权限。"
                    f"请检查模型名称和 API 端点，"
                    f"Coding Plan 端点: https://coding.dashscope.aliyuncs.com/v1，"
                    f"标准端点: https://dashscope.aliyuncs.com/compatible-mode/v1"
                )
            if "401" in error_str or "Unauthorized" in error_str:
                raise Exception("API Key 无效或已过期，请检查配置")
            raise Exception(f"Qwen API 调用失败: {error_str}")

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
            model=self.model_id or "deepseek-chat",
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