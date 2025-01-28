using System.Text.Json.Serialization;

namespace OpenQA.Selenium.DevTools.V130;

[JsonSerializable(typeof(ICommand))]
internal sealed partial class V130RequestSerializationContext : JsonSerializerContext;

[JsonSerializable(typeof(ICommand))]
internal sealed partial class V130ResponseSerializationContext : JsonSerializerContext;
